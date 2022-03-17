from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_rhino.artists import RhinoArtist
from compas_fofin.datastructures import CableMesh

from .cablemeshartist import RhinoCableMeshArtist


@plugin(category="ui", requires=["Rhino"])
def register_artists():
    RhinoArtist.register(CableMesh, RhinoCableMeshArtist, context="Rhino")
    print("Rhino FoFin artists registered.")


__all__ = [
    'RhinoCableMeshArtist',
]
