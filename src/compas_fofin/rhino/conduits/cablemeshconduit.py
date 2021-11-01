from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import BaseConduit

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector

from System.Drawing.Color import FromArgb

try:
    import Rhino

    from Rhino.Geometry import Line
    from Rhino.Geometry import Point3d

    basestring
except NameError:
    basestring = str


class ReactionConduit(BaseConduit):
    """Display conduit for CableMesh reactions
    """

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super(ReactionConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.1

    def CalculateBoundingBox(self, e):
        bbox = Rhino.Geometry.BoundingBox(-1000, -1000, -1000, 1000, 1000, 1000)
        e.IncludeBoundingBox(bbox)

    def DrawForeground(self, e):

        for vertex in self.cablemesh.vertices():
            ep = self.cablemesh.vertex_coordinates(vertex)
            r = self.cablemesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -self.scale)
            if length_vector(r) < self.tol:
                continue
            sp = add_vectors(ep, r)
            line = Line(Point3d(*ep), Point3d(*sp))
            e.Display.DrawArrow(line,
                                FromArgb(*self.color),
                                0,
                                self.arrow_size)


class LoadConduit(BaseConduit):
    """Display conduit for CableMesh loads.
    """

    def __init__(self, cablemesh, color, scale, tol, **kwargs):
        super(LoadConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.1

    def CalculateBoundingBox(self, e):
        bbox = Rhino.Geometry.BoundingBox(-1000, -1000, -1000, 1000, 1000, 1000)
        e.IncludeBoundingBox(bbox)

    def DrawForeground(self, e):
        for vertex in self.cablemesh.vertices():
            ep = self.cablemesh.vertex_coordinates(vertex)
            p = self.cablemesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            p = scale_vector(p, self.scale)
            if length_vector(p) < self.tol:
                continue
            sp = add_vectors(ep, p)
            line = Line(Point3d(*ep), Point3d(*sp))
            e.Display.DrawArrow(line,
                                FromArgb(*self.color),
                                0,
                                self.arrow_size)
