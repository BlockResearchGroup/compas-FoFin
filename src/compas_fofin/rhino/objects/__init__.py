from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin

from compas_fd.constraints import CurveConstraint
from compas_fd.constraints import LineConstraint
from compas_fd.constraints import CircleConstraint
from compas_fofin.datastructures import CableMesh

from compas_ui.rhino.objects import RhinoObject

from .cablemeshobject import RhinoCableMeshObject
from .lineconstraintobject import RhinoLineConstraintObject
from .circleconstraintobject import RhinoCircleConstraintObject
from .curveconstraintobject import RhinoCurveConstraintObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():

    RhinoObject.register(CurveConstraint, RhinoCurveConstraintObject, context="Rhino")
    RhinoObject.register(LineConstraint, RhinoLineConstraintObject, context="Rhino")
    RhinoObject.register(CircleConstraint, RhinoCircleConstraintObject, context="Rhino")
    RhinoObject.register(CableMesh, RhinoCableMeshObject, context="Rhino")

    print("FoFin Rhino Objects registered.")


__all__ = [
    "RhinoCableMeshObject",
    "RhinoLineConstraintObject",
    "RhinoCircleConstraintObject",
    "RhinoCurveConstraintObject",
]
