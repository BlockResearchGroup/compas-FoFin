from typing import Optional
from typing import Union

from compas.datastructures import Mesh
from compas_fd.constraints import Constraint  # noqa: F401


class CableMesh(Mesh):
    """The FoFin CableMesh."""

    @property
    def __data__(self) -> dict:
        data = super(CableMesh, self).__data__
        data["constraints"] = self.constraints
        return data

    @classmethod
    def __from_data__(cls, data: dict) -> "CableMesh":
        cablemesh = super(CableMesh, cls).__from_data__(data)
        cablemesh.constraints = data.get("constraints") or {}
        return cablemesh

    def __init__(self, constraints: Optional[list[Constraint]] = None, **kwargs) -> None:
        super(CableMesh, self).__init__(**kwargs)
        self.attributes.update(
            {
                "density": 1,
            }
        )
        self.default_vertex_attributes.update(
            is_support=False,
            constraint=None,
            px=0,
            py=0,
            pz=0,
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
        self.is_solved = False

    def vertex_constraint(self, vertex: int) -> Union[Constraint, None]:
        guid = self.vertex_attribute(vertex, "constraint")
        if guid:
            return self.constraints[guid]

    def update_constraints(self) -> None:
        for vertex in self.vertices():
            constraint = self.vertex_constraint(vertex)
            if constraint:
                constraint.location = self.vertex_point(vertex)
                constraint.project()
                self.vertex_attributes(vertex, "xyz", constraint.location)
