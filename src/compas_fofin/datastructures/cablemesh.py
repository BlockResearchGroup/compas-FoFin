from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fd.datastructures import CableMesh


class CableMesh(CableMesh):
    """The FoFin CableMesh.
    """

    def vertices_on_edge_loop(self, uv):
        edges = self.edge_loop(uv)
        if len(edges) == 1:
            return edges[0]
        vertices = [edge[0] for edge in edges]
        if edges[-1][1] != edges[0][0]:
            vertices.append(edges[-1][1])
        return vertices

    def corner_vertices(self):
        vertices = []
        if self.is_closed():
            for vertex in self.vertices():
                if self.vertex_degree(vertex) == 3:
                    vertices.append(vertex)
        else:
            for vertex in self.vertices_on_boundary():
                if self.vertex_degree(vertex) == 2:
                    vertices.append(vertex)
        return vertices
