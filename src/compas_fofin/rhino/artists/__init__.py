from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_rhino.artists import RhinoArtist

from compas_fofin.datastructures import CableMesh
from compas_fd.constraints import LineConstraint
from compas_fd.constraints import CircleConstraint
from compas_fd.constraints import CurveConstraint

from .cablemeshartist import RhinoCableMeshArtist
from .lineconstraintartist import RhinoLineConstraintArtist
from .circleconstraintartist import RhinoCircleConstraintArtist
from .curveconstraintartist import RhinoCurveConstraintArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():

    RhinoArtist.register(CurveConstraint, RhinoCurveConstraintArtist, context="Rhino")
    RhinoArtist.register(LineConstraint, RhinoLineConstraintArtist, context="Rhino")
    RhinoArtist.register(CircleConstraint, RhinoCircleConstraintArtist, context="Rhino")
    RhinoArtist.register(CableMesh, RhinoCableMeshArtist, context="Rhino")

    print("FoFin Rhino Artists registered.")


__all__ = [
    "RhinoCableMeshArtist",
    "RhinoLineConstraintArtist",
    "RhinoCircleConstraintArtist",
    "RhinoCurveConstraintArtist",
]
