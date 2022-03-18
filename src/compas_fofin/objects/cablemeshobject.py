from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.objects import MeshObject


class CableMeshObject(MeshObject):
    """Base object for representing a cable mesh in a scene.
    """

    def __init__(self, *args, **kwargs):
        super(CableMeshObject, self).__init__(*args, **kwargs)
