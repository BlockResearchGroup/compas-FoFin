from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_fofin.datastructures import CableMesh
from compas_ui.rhino.objects import RhinoObject

from .cablemeshobject import RhinoCableMeshObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(CableMesh, RhinoCableMeshObject, context="Rhino")
    print("Rhino FoFin objects registered.")


__all__ = [
    'RhinoCableMeshObject'
]
