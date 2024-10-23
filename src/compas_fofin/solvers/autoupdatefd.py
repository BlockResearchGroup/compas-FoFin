from typing import List
from typing import Union

from compas.geometry import Vector
from compas_fd.constraints import Constraint
from compas_fd.loads import SelfweightCalculator
from compas_fd.solvers.fd_constrained_numpy import _is_converged_disp
from compas_fd.solvers.fd_constrained_numpy import _is_converged_residuals
from compas_fd.solvers.fd_constrained_numpy import _post_process_fd
from compas_fd.solvers.fd_constrained_numpy import _solve_fd
from compas_fd.solvers.fd_constrained_numpy import _update_constraints
from compas_fd.solvers.fd_numerical_data import FDNumericalData
from compas_fofin.datastructures import CableMesh


class AutoUpdateFD:
    def __init__(
        self,
        cablemesh: CableMesh,
        kmax: int = 100,
        tol_res: float = 1e-3,
        tol_disp: float = 1e-3,
        damping: float = 0.1,
    ):
        self.cablemesh = cablemesh
        self.kmax = kmax
        self.tol_res = tol_res
        self.tol_disp = tol_disp
        self.damping = damping
        self._numdata = None
        self._constraints = None
        self._selfweight = None
        self._conduit_edges = None
        self._conduit_reactions = None

    def __call__(self):
        self.solve()
        self.cablemesh.is_solved = True

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

    def solve(self):
        for k in range(self.kmax):
            print(k)
            xyz_prev = self.numdata.xyz
            _solve_fd(self.numdata, self.selfweight)
            _update_constraints(self.numdata, self.constraints, self.damping)
            if _is_converged_residuals(self.numdata.tangent_residuals, self.tol_res) and _is_converged_disp(xyz_prev, self.numdata.xyz, self.tol_disp):
                break

        _solve_fd(self.numdata, self.selfweight)
        _post_process_fd(self.numdata)

        for index, vertex in enumerate(self.cablemesh.vertices()):
            self.cablemesh.vertex_attribute(vertex, "x", self.numdata.xyz[index, 0])
            self.cablemesh.vertex_attribute(vertex, "y", self.numdata.xyz[index, 1])
            self.cablemesh.vertex_attribute(vertex, "z", self.numdata.xyz[index, 2])
            self.cablemesh.vertex_attribute(vertex, "_residual", Vector(*self.numdata.residuals[index]))

        for index, edge in enumerate(self.cablemesh.edges()):
            self.cablemesh.edge_attribute(edge, "_f", self.numdata.forces[index, 0])

        self.cablemesh.is_solved = True
