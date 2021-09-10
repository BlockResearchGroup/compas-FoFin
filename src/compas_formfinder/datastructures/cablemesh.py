from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.datastructures import CableMesh as FdMesh
from compas.geometry import angle_vectors


__all__ = ['CableMesh']


class CableMesh(FdMesh):
    """The FF CableMesh.
    """

    def vertices_on_edge_loop(self, uv):
        edges = self.edge_loop(uv)
        if len(edges) == 1:
            return edges[0]
        vertices = [edge[0] for edge in edges]
        if edges[-1][1] != edges[0][0]:
            vertices.append(edges[-1][1])
        return vertices

    def corner_vertices(self, tol=160):
        vkeys = []
        for key in self.vertices_on_boundary():
            if self.vertex_degree(key) == 2:
                vkeys.append(key)
            else:
                nbrs = []
                for nkey in self.vertex_neighbors(key):
                    if self.is_edge_on_boundary(key, nkey):
                        nbrs.append(nkey)
                u = (self.edge_vector(key, nbrs[0]))
                v = (self.edge_vector(key, nbrs[1]))
                if angle_vectors(u, v, deg=True) < tol:
                    vkeys.append(key)
        return vkeys
