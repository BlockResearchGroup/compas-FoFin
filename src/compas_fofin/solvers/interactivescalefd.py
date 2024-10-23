from typing import List
from typing import Tuple
from typing import Union

import Rhino  # type: ignore
from numpy import full_like

import compas_rhino.conversions
from compas_fd.constraints import Constraint
from compas_fd.loads import SelfweightCalculator
from compas_fd.solvers.fd_constrained_numpy import _is_converged_disp
from compas_fd.solvers.fd_constrained_numpy import _is_converged_residuals
from compas_fd.solvers.fd_constrained_numpy import _solve_fd
from compas_fd.solvers.fd_constrained_numpy import _update_constraints
from compas_fd.solvers.fd_numerical_data import FDNumericalData
from compas_fofin.conduits import EdgesConduit
from compas_fofin.datastructures import CableMesh


class InteractiveScaleFD:
    def __init__(
        self,
        cablemesh: CableMesh,
        edges: List[Tuple[int, int]],
        kmax: int = 100,
        tol_res: float = 1e-3,
        tol_disp: float = 1e-3,
        damping: float = 0.1,
    ):
        self.cablemesh = cablemesh
        self.edges = edges
        self.kmax = kmax
        self.tol_res = tol_res
        self.tol_disp = tol_disp
        self.damping = damping
        self.scale = 1.0
        self._indexes = None
        self._numdata = None
        self._constraints = None
        self._selfweight = None
        self._q0 = None
        self._scale = None
        self._conduit_edges = None
        self._conduit_reactions = None

    def __call__(self):
        self.start()
        self.stop()

    @property
    def indexes(self):
        if self._indexes is None:
            uv_index = {(u, v): index for index, (u, v) in enumerate(self.cablemesh.edges())}
            uv_index.update({(v, u): index for index, (u, v) in enumerate(self.cablemesh.edges())})
            self._indexes = [uv_index[uv] for uv in self.edges]
        return self._indexes

    @property
    def conduit_edges(self) -> EdgesConduit:
        if not self._conduit_edges:
            self._conduit_edges = EdgesConduit(self.numdata.xyz, self.numdata.edges, thickness=1)
        return self._conduit_edges

    @property
    def numdata(self) -> FDNumericalData:
        if self._numdata is None:
            vertex_index = self.cablemesh.vertex_index()
            vertices = self.cablemesh.vertices_attributes("xyz")
            loads = [self.cablemesh.vertex_attributes(vertex, ["px", "py", "pz"]) or [0, 0, 0] for vertex in self.cablemesh.vertices()]
            fixed = [vertex_index[vertex] for vertex in self.cablemesh.vertices_where(is_support=True)]
            edges = [(vertex_index[u], vertex_index[v]) for u, v in self.cablemesh.edges()]
            forcedensities = list(self.cablemesh.edges_attribute("q"))
            self._numdata = FDNumericalData.from_params(vertices, fixed, edges, forcedensities, loads)
        return self._numdata

    @property
    def constraints(self) -> List[Union[None, Constraint]]:
        if self._constraints is None:
            self._constraints = [None] * self.numdata.xyz.shape[0]
            for index, vertex in enumerate(self.cablemesh.vertices()):
                guid = self.cablemesh.vertex_attribute(vertex, "constraint")
                if guid:
                    constraint = self.cablemesh.constraints[guid]
                    self._constraints[index] = constraint
        return self._constraints

    @property
    def selfweight(self) -> SelfweightCalculator:
        if self._selfweight is None:
            self._selfweight = SelfweightCalculator(
                self.cablemesh,
                self.cablemesh.attributes["density"],
                thickness_attr_name="thickness",
            )
        return self._selfweight

    @property
    def q0(self):
        if self._q0 is None:
            self._q0 = self.numdata.q[self.indexes]
        return self._q0

    @property
    def q(self):
        return full_like(self.q0, self.scale) * self.q0

    def _update(self) -> None:
        self.numdata.update_forcedensities(self.indexes, self.q)

        for k in range(self.kmax):
            print(k)
            xyz_prev = self.numdata.xyz
            _solve_fd(self.numdata, self.selfweight)
            _update_constraints(self.numdata, self.constraints, self.damping)
            if _is_converged_residuals(self.numdata.tangent_residuals, self.tol_res) and _is_converged_disp(xyz_prev, self.numdata.xyz, self.tol_disp):
                break

        _solve_fd(self.numdata, self.selfweight)

    def start(self):
        Rhino.ApplicationSettings.ModelAidSettings.Ortho = True

        def on_dynamic_draw(sender, e):
            self.conduit_edges.disable()
            p2 = compas_rhino.conversions.point_to_compas(e.CurrentPoint)
            v02 = p2 - p0
            sign = +1 if v02.dot(v01) > 0 else -1
            self.scale = sign * v02.length / v01.length
            self._update()
            self.conduit_edges.enable()

        get_p0 = Rhino.Input.Custom.GetPoint()
        get_p0.SetCommandPrompt("Select base point")
        get_p0.Get()
        rhino_p0 = get_p0.Point()
        p0 = compas_rhino.conversions.point_to_compas(rhino_p0)

        get_p1 = Rhino.Input.Custom.GetPoint()
        get_p1.DrawLineFromPoint(rhino_p0, True)
        get_p1.SetCommandPrompt("Select reference 1")
        get_p1.Get()
        rhino_p1 = get_p1.Point()
        p1 = compas_rhino.conversions.point_to_compas(rhino_p1)

        v01 = p1 - p0

        get_p2 = Rhino.Input.Custom.GetPoint()
        get_p2.DrawLineFromPoint(rhino_p0, True)
        get_p2.SetCommandPrompt("Select reference 2")
        get_p2.DynamicDraw += on_dynamic_draw
        get_p2.Get()
        rhino_p2 = get_p2.Point()
        p2 = compas_rhino.conversions.point_to_compas(rhino_p2)

        v02 = p2 - p0

        sign = +1 if v02.dot(v01) > 0 else -1
        self.scale = sign * v02.length / v01.length

    def stop(self):
        self.cablemesh.is_solved = True

        self.numdata.update_forcedensities(self.indexes, self.q)
        for index, edge in enumerate(self.cablemesh.edges()):
            self.cablemesh.edge_attribute(edge, "q", self.numdata.q[index, 0])

        self.conduit_edges.disable()
        del self._conduit_edges
        self._conduit_edges = None

    # def solve(self):
    #     self.numdata.update_forcedensities(self.indexes, self.q)

    #     for k in range(self.kmax):
    #         print(k)
    #         xyz_prev = self.numdata.xyz
    #         _solve_fd(self.numdata, self.selfweight)
    #         _update_constraints(self.numdata, self.constraints, self.damping)
    #         if _is_converged_residuals(self.numdata.tangent_residuals, self.tol_res) and _is_converged_disp(xyz_prev, self.numdata.xyz, self.tol_disp):
    #             break

    #     _solve_fd(self.numdata, self.selfweight)
    #     _post_process_fd(self.numdata)

    #     # update Qs

    #     for index, vertex in enumerate(self.cablemesh.vertices()):
    #         self.cablemesh.vertex_attribute(vertex, "x", self.numdata.xyz[index, 0])
    #         self.cablemesh.vertex_attribute(vertex, "y", self.numdata.xyz[index, 1])
    #         self.cablemesh.vertex_attribute(vertex, "z", self.numdata.xyz[index, 2])
    #         self.cablemesh.vertex_attribute(vertex, "_residual", Vector(*self.numdata.residuals[index]))

    #     for index, edge in enumerate(self.cablemesh.edges()):
    #         self.cablemesh.edge_attribute(edge, "_f", self.numdata.forces[index, 0])
    #         self.cablemesh.edge_attribute(edge, "q", self.numdata.q[index, 0])
