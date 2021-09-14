from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists import MeshArtist


__all__ = ['CableMeshArtist']


class CableMeshArtist(MeshArtist):
    """Artist for visualizing a CableMesh in the Rhino model space."""

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
