from compas.plugins import plugin
from compas.scene.context import register
from compas_fofin.datastructures import CableMesh

from .cablemeshobject import RhinoCableMeshObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(CableMesh, RhinoCableMeshObject, context="Rhino")
    print("FoFin SceneObjects for Rhino registered.")
