from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.datastructures import CableMesh

from compas_rhino.artists import RhinoArtist
from .cablemeshartist import CableMeshArtist

RhinoArtist.register(CableMesh, CableMeshArtist, context='Rhino')
