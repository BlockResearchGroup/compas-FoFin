from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Rhino.Geometry import Line
from Rhino.Geometry import Point3d
from System.Drawing import Color

from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import dot_vectors
from compas.geometry import length_vector_sqrd
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas_rhino.conduits import BaseConduit


class ReactionConduit(BaseConduit):
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

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super(ReactionConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.2

    def PostDrawObjects(self, e):
        color = Color.FromArgb(*self.color)
        scale = self.scale
        tol2 = self.tol**2
        mesh = self.cablemesh
        lines = []
        for vertex in mesh.vertices_where(is_anchor=True):
            start = mesh.vertex_attributes(vertex, "xyz")
            reaction = mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"])
            nbrs = mesh.vertex_neighbors(vertex)
            points = mesh.vertices_attributes("xyz", keys=nbrs)
            vectors = [subtract_vectors(point, start) for point in points]
            vector = centroid_points(vectors)
            reaction = scale_vector(reaction, -scale)
            if length_vector_sqrd(reaction) < tol2:
                continue
            if dot_vectors(vector, reaction) > 0:
                end = subtract_vectors(start, reaction)
                line = Line(Point3d(*end), Point3d(*start))
            else:
                end = add_vectors(start, reaction)
                line = Line(Point3d(*start), Point3d(*end))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)


class LoadConduit(BaseConduit):
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

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super(LoadConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.3

    def PostDrawObjects(self, e):
        color = Color.FromArgb(*self.color)
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
            line = Line(Point3d(*start), Point3d(*end))
            lines.append(line)
            # e.Display.DrawArrow(line, color, 0, size)
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

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super(SelfweightConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = Color.FromArgb(*self.color)
        lines = []
        for vertex in self.cablemesh.vertices():
            start = self.cablemesh.vertex_coordinates(vertex)
            thickness = self.cablemesh.vertex_attribute(vertex, "t")
            area = self.cablemesh.vertex_area(vertex)
            weight = thickness * area * self.scale
            if weight < self.tol:
                continue
            end = [start[0], start[1], start[2] - weight]
            line = Line(Point3d(*start), Point3d(*end))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)


class PipeConduit(BaseConduit):
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

    def __init__(self, xyz, edges, values, color, **kwargs):
        super(PipeConduit, self).__init__(**kwargs)
        self.xyz = xyz or {}
        self.edges = edges or []
        self.values = values or {}
        self.color = color or {}

    def PostDrawObjects(self, e):
        for edge in self.edges:
            u, v = edge
            sp = self.xyz[u]
            ep = self.xyz[v]
            thickness = int(abs(self.values[edge]))
            e.Display.DrawLine(Point3d(*sp), Point3d(*ep), Color.FromArgb(*self.color[edge]), thickness)


class EdgeConduit(BaseConduit):
    """Display conduit for CableMesh edges as lines.

    Parameters
    ----------
    xyz : list of list of float
        The vertex coordinates.
    edges : list of tuple of int
        List of pairs of indices into the list of vertex coordinates.

    """

    def __init__(self, xyz, edges, **kwargs):
        super(EdgeConduit, self).__init__(**kwargs)
        self.xyz = xyz
        self.edges = edges

    def PostDrawObjects(self, e):
        color = Color.Black
        for i, j in self.edges:
            sp = self.xyz[i]
            ep = self.xyz[j]
            e.Display.DrawLine(Point3d(*sp), Point3d(*ep), color)
