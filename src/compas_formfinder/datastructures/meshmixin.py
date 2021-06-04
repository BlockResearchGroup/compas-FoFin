from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from compas.utilities import pairwise
from compas.geometry import angle_vectors


__all__ = ['MeshMixin']


class MeshMixin(object):
    """Mixin for all mesh-based data structure in RV2."""

    def edge_loop(self, uv):
        if self.is_edge_on_boundary(*uv):
            return self._edge_loop_on_boundary(uv)

        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        return edges

    def _edge_loop_on_boundary(self, uv):
        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, 'is_fixed'):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        return edges

    def edge_strip(self, uv):
        edges = []
        v, u = uv
        while True:
            edges.append((u, v))
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        edges[:] = [(u, v) for v, u in edges[::-1]]
        u, v = uv
        while True:
            fkey = self.halfedge[u][v]
            if fkey is None:
                break
            vertices = self.face_vertices(fkey)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
            edges.append((u, v))
        return edges

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
