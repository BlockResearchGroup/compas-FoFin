from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import BaseConduit

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector_sqrd

from System.Drawing import Color

from Rhino.Geometry import Line
from Rhino.Geometry import Point3d


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
        self.arrow_size = 0.1

    def DrawForeground(self, e):
        color = Color.FromArgb(*self.color)
        size = self.arrow_size
        scale = self.scale
        tol2 = self.tol ** 2
        for vertex in self.cablemesh.vertices_where(is_anchor=True):
            sp = self.cablemesh.vertex_attributes(vertex, ['x', 'y', 'z'])
            r = self.cablemesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -scale)
            if length_vector_sqrd(r) < tol2:
                continue
            ep = add_vectors(sp, r)
            line = Line(Point3d(*sp), Point3d(*ep))
            e.Display.DrawArrow(line, color, 0, size)


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
        self.color = Color.FromArgb(*color)
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.1

    def DrawForeground(self, e):
        color = self.color
        size = self.arrow_size
        scale = self.scale
        tol2 = self.tol ** 2
        mesh = self.cablemesh
        for vertex in mesh.vertices():
            ep = mesh.vertex_coordinates(vertex)
            p = mesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            p = scale_vector(p, scale)
            if length_vector_sqrd(p) < tol2:
                continue
            sp = add_vectors(ep, p)
            line = Line(Point3d(*ep), Point3d(*sp))
            e.Display.DrawArrow(line, color, 0, size)


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

    def DrawForeground(self, e):
        for edge in self.edges:
            u, v = edge
            sp = self.xyz[u]
            ep = self.xyz[v]
            thickness = int(abs(self.values[edge]))
            e.Display.DrawLine(Point3d(*sp),
                               Point3d(*ep),
                               Color.FromArgb(*self.color[edge]),
                               thickness)
