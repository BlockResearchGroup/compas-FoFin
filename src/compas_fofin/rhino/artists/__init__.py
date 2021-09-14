from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.datastructures import CableMesh

from compas_rhino.artists import BaseArtist
from .cablemeshartist import CableMeshArtist

BaseArtist.register(CableMesh, CableMeshArtist)

__all__ = [
    'CableMeshArtist'
]
