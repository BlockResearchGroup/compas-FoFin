from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.datastructures import CableMesh

from .cablemeshobject import CableMeshObject
from .meshobject import MeshObject

MeshObject.register(CableMesh, CableMeshObject)

