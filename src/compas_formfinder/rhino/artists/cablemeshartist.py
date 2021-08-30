from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import sqrt

import compas_rhino

from .meshartist import MeshArtist


__all__ = ['CableMeshArtist']


class CableMeshArtist(MeshArtist):
    """Artist for visualizing form diagrams in the Rhino model space."""

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xy') + [0.0] for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz


    def draw_pipes(self, edges, color, scale, tol):
        vertex_xyz = self.vertex_xyz
        cylinders = []
        for edge in edges:
            u, v = edge
            start = vertex_xyz[u]
            end = vertex_xyz[v]
            force = self.mesh.edge_attribute(edge, 'f')
            force = scale * force
            if force < tol:
                continue
            radius = sqrt(force / pi)
            if isinstance(color, dict):
                pipe_color = color[edge]
            else:
                pipe_color = color
            cylinders.append({
                'start': start,
                'end': end,
                'radius': radius,
                'color': pipe_color
            })
        return compas_rhino.draw_cylinders(cylinders, layer=self.layer, clear=False, redraw=False)
