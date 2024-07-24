from compas.datastructures import Mesh
from compas.geometry import Vector


class CableMesh(Mesh):
    """The FoFin CableMesh."""

    def __init__(self, *args, **kwargs):
        super(CableMesh, self).__init__(*args, **kwargs)
        self.default_vertex_attributes.update(
            is_anchor=False,
            is_constrained=False,
            residual=None,
            load=None,
            thickness=0,
        )
        self.default_edge_attributes.update(
            q=1.0,
            f=0.0,
            l=0.0,
            l0=0.0,
            E=0.0,
            radius=0.0,
            _q=0.0,
            _f=0.0,
            _l=0.0,
        )
        self.default_face_attributes.update({})

    def vertex_residual(self, vertex):
        residual = self.vertex_attribute(vertex, "residual")
        if not residual:
            residual = Vector(0, 0, 0)
        return residual

    def vertex_load(self, vertex):
        load = self.vertex_attribute(vertex, "load")
        if not load:
            load = Vector(0, 0, 0)
        return load

    def edge_force(self, edge):
        vector = self.edge_direction()
        vector.scale(self.edge_attribute(edge, "_f"))
        return vector

    # def vertices_on_edge_loop(self, uv):
    #     edges = self.edge_loop(uv)
    #     if len(edges) == 1:
    #         return edges[0]
    #     vertices = [edge[0] for edge in edges]
    #     if edges[-1][1] != edges[0][0]:
    #         vertices.append(edges[-1][1])
    #     return vertices

    # def corner_vertices(self):
    #     vertices = []
    #     if self.is_closed():
    #         for vertex in self.vertices():
    #             if self.vertex_degree(vertex) == 3:
    #                 vertices.append(vertex)
    #     else:
    #         for vertex in self.vertices_on_boundary():
    #             if self.vertex_degree(vertex) == 2:
    #                 vertices.append(vertex)
    #     return vertices
