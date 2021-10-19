from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import BaseConduit

from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector

from System.Collections.Generic import List
from System.Drawing.Color import FromArgb

try:
    import Rhino

    from Rhino.ApplicationSettings import ModelAidSettings
    from Rhino.Geometry import Line
    from Rhino.Geometry import Point3d

    basestring
except NameError:
    basestring = str


__all__ = ['CableMeshConduit']


class CableMeshConduit(BaseConduit):
    """ A Rhino display conduit for CableMesh.
    """

    def __init__(self, cablemesh, scale, tol, **kwargs):
        super(CableMeshConduit, self).__init__(**kwargs)
        self.cablemesh = cablemesh
        self.scale = scale
        self.tol = tol
        self._color_reactions = FromArgb(0, 200, 0)
        self._color_residuals = FromArgb(0, 255, 255)
        self._color_loads = FromArgb(0, 80, 255)
        self.vertex_xyz = self.cablemesh.vertex_xyz

    def DrawReactions(self, e):
        print('conduit')
        for vertex in self.cablemesh.vertices():
            ep = self.vertex_xyz[vertex]
            r = self.cablemesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -self.scale)
            if length_vector(r) < self.tol:
                continue
            sp = add_vectors(ep, r)
            line = Line(Point3d(*sp), Point3d(*ep))
            e.Display.DrawArrow(line, self._color_reactions, 2)

    def DrawResiduals(self, e):
        pass

    def DrawLoads(self, e):
        pass
