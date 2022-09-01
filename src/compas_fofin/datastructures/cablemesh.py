from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Polygon
from compas_fd.datastructures import CableMesh


class CableMesh(CableMesh):
    """The FoFin CableMesh."""

    def __init__(self, *args, **kwargs):
        super(CableMesh, self).__init__(*args, **kwargs)
        self.default_vertex_attributes.update({})
        self.default_edge_attributes.update(
            {
                "q": 1.0,
                "f": 0.0,
                "l": 0.0,
                "l0": 0.0,
                "E": 0.0,
                "radius": 0.0,
                "_q": 0.0,
                "_f": 0.0,
                "_l": 0.0,
            }
        )
        self.default_face_attributes.update({})

    def vertex_point(self, vertex):
        return Point(*self.vertex_coordinates(vertex))

    def vertex_residual(self, vertex):
        return Vector(*self.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))

    def vertex_load(self, vertex):
        return Vector(*self.vertex_attributes(vertex, ["px", "py", "pz"]))

    def edge_line(self, edge):
        return Line(self.vertex_coordinates(edge[0]), self.vertex_coordinates(edge[1]))

    def edge_vector(self, edge):
        return Vector.from_start_end(
            self.vertex_coordinates(edge[0]), self.vertex_coordinates(edge[1])
        )

    def edge_force(self, edge):
        vector = self.edge_vector()
        vector.unitize()
        vector.scale(self.edge_attribute(edge, "_f"))
        return vector

    def face_polygon(self, face):
        return Polygon(self.face_coordinates(face))

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
