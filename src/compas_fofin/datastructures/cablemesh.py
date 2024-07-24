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
        self.constraints = {}

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
