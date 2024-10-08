from compas.plugins import plugin
from compas.scene.context import register

from compas_fofin.datastructures import CableMesh
from compas_fd.constraints import Constraint

from .cablemeshobject import RhinoCableMeshObject
from .constraintobject import RhinoConstraintObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(CableMesh, RhinoCableMeshObject, context="Rhino")
    register(Constraint, RhinoConstraintObject, context="Rhino")


__all__ = [
    "RhinoCableMeshObject",
    "RhinoConstraintObject",
]
