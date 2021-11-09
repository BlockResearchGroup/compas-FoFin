from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import sqrt

from compas_rhino.conduits import BaseConduit

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector_sqrd
from compas.geometry import distance_point_point

from System.Drawing.Color import FromArgb

import Rhino
from Rhino.Display import DisplayMaterial
from Rhino.Geometry import Brep
from Rhino.Geometry import Cylinder
from Rhino.Geometry import Circle
from Rhino.Geometry import Line
from Rhino.Geometry import Plane
from Rhino.Geometry import Point3d
from Rhino.Geometry import Vector3d


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
        for vertex in self.cablemesh.vertices():
            ep = self.cablemesh.vertex_coordinates(vertex)
            r = self.cablemesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -self.scale)
            if length_vector_sqrd(r) < self.tol ** 2:
                continue
            sp = add_vectors(ep, r)
            line = Line(Point3d(*ep), Point3d(*sp))
            e.Display.DrawArrow(line,
                                FromArgb(*self.color),
                                0,
                                self.arrow_size)


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
        self.arrow_size = 0.1

    def DrawForeground(self, e):
        for vertex in self.cablemesh.vertices():
            ep = self.cablemesh.vertex_coordinates(vertex)
            p = self.cablemesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            p = scale_vector(p, self.scale)
            if length_vector_sqrd(p) < self.tol ** 2:
                continue
            sp = add_vectors(ep, p)
            line = Line(Point3d(*ep), Point3d(*sp))
            e.Display.DrawArrow(line,
                                FromArgb(*self.color),
                                0,
                                self.arrow_size)


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
                               FromArgb(*self.color[edge]),
                               thickness)
