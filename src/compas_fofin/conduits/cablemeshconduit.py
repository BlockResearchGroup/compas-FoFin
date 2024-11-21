from typing import Annotated
from typing import List
from typing import Tuple

import Rhino  # type: ignore
import System  # type: ignore

import compas_rhino.conversions
from compas.colors import Color
from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import dot_vectors
from compas.geometry import length_vector_sqrd
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas_fofin.datastructures import CableMesh
from compas_rhino.conduits import BaseConduit


class ReactionsConduit(BaseConduit):
    """Display conduit for CableMesh reactions

    Parameters
    ----------
    cablemesh : :class:`compas_fofin.datastructures.CableMesh`
        The cablemesh.
    color : rgb tuple
        The color of the reaction forces.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a reaction force vector.
    """

    cablemesh: CableMesh
    color: Color
    scale: float
    tol: float
    arrow_size: float

    def __init__(self, cablemesh, color, scale, tol, arrow_size=1.0, **kwargs):
        super().__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = arrow_size

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)
        scale = self.scale
        tol2 = self.tol**2
        mesh: CableMesh = self.cablemesh

        for vertex in mesh.vertices_where(is_support=True):
            start = mesh.vertex_attributes(vertex, "xyz")
            reaction = mesh.vertex_attribute(vertex, "_residual")
            nbrs = mesh.vertex_neighbors(vertex)
            points = mesh.vertices_attributes("xyz", keys=nbrs)
            vectors = [subtract_vectors(point, start) for point in points]
            vector = centroid_points(vectors)
            reaction = scale_vector(reaction, -scale)

            if length_vector_sqrd(reaction) < tol2:
                continue

            if dot_vectors(vector, reaction) > 0:
                end = subtract_vectors(start, reaction)
                line = Rhino.Geometry.Line(
                    Rhino.Geometry.Point3d(*end),
                    Rhino.Geometry.Point3d(*start),
                )
            else:
                end = add_vectors(start, reaction)
                line = Rhino.Geometry.Line(
                    Rhino.Geometry.Point3d(*start),
                    Rhino.Geometry.Point3d(*end),
                )

            e.Display.DrawArrow(line, color, 0.0, 0.1)


class LoadsConduit(BaseConduit):
    """Display conduit for CableMesh loads.

    Parameters
    ----------
    cablemesh : :class:`compas_fofin.datastructures.CableMesh`
        The cablemesh.
    color : rgb tuple
        The color of the loads.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a load vector.
    """

    cablemesh: CableMesh
    color: Color
    scale: float
    tol: float
    arrow_size: float

    def __init__(self, cablemesh, color, scale, tol, arrow_size=1.0, **kwargs):
        super().__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = arrow_size

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)
        scale = self.scale
        tol2 = self.tol**2

        lines = []

        for vertex in self.cablemesh.vertices():
            start = self.cablemesh.vertex_coordinates(vertex)
            load = self.cablemesh.vertex_attributes(vertex, ["px", "py", "pz"])
            load = scale_vector(load, scale)
            if length_vector_sqrd(load) < tol2:
                continue

            end = add_vectors(start, load)
            line = Rhino.Geometry.Line(Rhino.Geometry.Point3d(*start), Rhino.Geometry.Point3d(*end))
            lines.append(line)

        if lines:
            e.Display.DrawArrows(lines, color)


class SelfweightConduit(BaseConduit):
    """Display conduit for CableMesh selfweight vectors.

    Parameters
    ----------
    cablemesh : :class:`compas_fofin.datastructures.CableMesh`
        The cablemesh.
    color : rgb tuple
        The color of the vectors.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a selfweight vector.
    """

    cablemesh: CableMesh
    color: Color
    scale: float
    tol: float
    arrow_size: float

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super().__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)

        lines = []

        for vertex in self.cablemesh.vertices():
            start = self.cablemesh.vertex_coordinates(vertex)
            thickness = self.cablemesh.vertex_attribute(vertex, "thickness")
            area = self.cablemesh.vertex_area(vertex)
            weight = thickness * area * self.scale
            if weight < self.tol:
                continue

            end = [start[0], start[1], start[2] - weight]
            line = Rhino.Geometry.Line(Rhino.Geometry.Point3d(*start), Rhino.Geometry.Point3d(*end))
            lines.append(line)

        if lines:
            e.Display.DrawArrows(lines, color)


class ThickEdgesConduit(BaseConduit):
    """Display conduit for CableMesh pipes as thickened lines.

    Parameters
    ----------
    xyz : list of list of float
        The vertex coordinates.
    edges : list of tuple of int
        List of pairs of indices into the list of vertex coordinates.
    values : dict
        Mapping between edges and thicknesses.
    color : dict
        Mapping between edges and colors.
    """

    xyz: List[Annotated[List[float], 3]]
    edges: List[Tuple[int, int]]

    def __init__(self, xyz, edges, forces, tmax=10, **kwargs):
        super().__init__(**kwargs)
        self.xyz = xyz
        self.edges = edges
        self.color_tension = Color.red()
        self.color_compression = Color.blue()
        self._tmax = tmax
        self._thickness = None
        self._color = None
        self._forces = None
        self.forces = forces

    @property
    def tmax(self) -> int:
        return self._tmax

    @tmax.setter
    def tmax(self, value: int) -> None:
        if value != self._tmax:
            scale = value / self._tmax
            self._tmax = value
            if self._thickness is not None:
                self._thickness[:] = [scale * t for t in self._thickness]

    @property
    def forces(self) -> List[float]:
        return self._forces or []

    @forces.setter
    def forces(self, values) -> None:
        self._forces = values
        self.compute_thickness_and_color()

    @property
    def thickness(self) -> List[float]:
        return self._thickness or []

    @property
    def color(self) -> List[Color]:
        return self._color or []

    def compute_thickness_and_color(self) -> None:
        magnitudes = [abs(f) for f in self.forces]
        fmin = min(magnitudes)
        fmax = max(magnitudes)
        fspan = fmax - fmin
        thickness = []
        color = []
        for force, magnitude in zip(self.forces, magnitudes):
            t = self.tmax * (magnitude - fmin) / fspan
            c = self.color_tension if force > 0 else self.color_compression
            thickness.append(t)
            color.append(c)
        self._thickness = thickness
        self._color = color

    def PostDrawObjects(self, e):
        for edge, thickness, color in zip(self.edges, self.thickness, self.color):
            u, v = edge
            sp = self.xyz[u]
            ep = self.xyz[v]
            e.Display.DrawLine(
                Rhino.Geometry.Point3d(*sp),
                Rhino.Geometry.Point3d(*ep),
                System.Drawing.Color.FromArgb(*color.rgb255),
                int(abs(thickness)),
            )


class EdgesConduit(BaseConduit):
    """Display conduit for CableMesh edges as lines.

    Parameters
    ----------
    xyz : list of list of float
        The vertex coordinates.
    edges : list of tuple of int
        List of pairs of indices into the list of vertex coordinates.

    """

    xyz: List[Annotated[List[float], 3]]
    edges: List[Tuple[int, int]]
    thickness: int

    def __init__(self, xyz, edges, thickness=1, color=None, **kwargs):
        super().__init__(**kwargs)
        self.xyz = xyz
        self.edges = edges
        self.thickness = thickness
        self.color = color or Color(0, 0, 0)

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)
        lines = []
        for i, j in self.edges:
            sp = self.xyz[i]
            ep = self.xyz[j]
            lines.append(
                Rhino.Geometry.Line(
                    Rhino.Geometry.Point3d(*sp),
                    Rhino.Geometry.Point3d(*ep),
                )
            )

        if lines:
            e.Display.DrawLines(lines, color, self.thickness)


class FacesConduit(BaseConduit):
    def __init__(self):
        pass


class MeshConduit(BaseConduit):
    mesh: CableMesh
    color: Color

    def __init__(self, mesh, color, **kwargs):
        super().__init__(**kwargs)
        self.mesh = mesh
        self.color = color

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)
        mesh = compas_rhino.conversions.mesh_to_rhino(self.mesh)
        e.Display.DrawMeshShaded(mesh, Rhino.Display.DisplayMaterial(color))
