from compas.datastructures import Mesh
from compas.geometry import Vector


class CableMesh(Mesh):
    """The FoFin CableMesh."""

    @property
    def __data__(self):
        data = super(CableMesh, self).__data__
        data["constraints"] = self.constraints
        return data

    @classmethod
    def __from_data__(cls, data):
        cablemesh = super(CableMesh, cls).__from_data__(data)
        cablemesh.constraints = data["constraints"]
        return cablemesh

    def __init__(self, constraints=None, **kwargs):
        super(CableMesh, self).__init__(**kwargs)
        self.default_vertex_attributes.update(
            is_anchor=False,
            is_constrained=False,
            constraint=None,
            load=None,
            thickness=0,
            # computed values
            _residual=None,
        )
        self.default_edge_attributes.update(
            q=1.0,
            f=0.0,
            l=0.0,
            l0=0.0,
            E=0.0,
            radius=0.0,
            # computed stuff
            _f=0.0,
        )
        self.default_face_attributes.update({})
        self.constraints = constraints or {}

    # def vertex_residual(self, vertex):
    #     residual = self.vertex_attribute(vertex, "_residual")
    #     return residual

    # def vertex_load(self, vertex):
    #     load = self.vertex_attribute(vertex, "load")
    #     return load
