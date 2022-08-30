from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_rhino.artists import RhinoArtist

from compas_fofin.datastructures import CableMesh
from compas_fd.constraints import LineConstraint

from .cablemeshartist import RhinoCableMeshArtist
from .lineconstraintartist import RhinoLineConstraintArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():

    RhinoArtist.register(LineConstraint, RhinoLineConstraintArtist, context="Rhino")
    RhinoArtist.register(CableMesh, RhinoCableMeshArtist, context="Rhino")

    print("FoFin Rhino Artists registered.")


__all__ = [
    "RhinoCableMeshArtist",
    "RhinoLineConstraintArtist",
]
