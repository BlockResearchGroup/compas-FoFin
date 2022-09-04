from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas_ui.rhino.objects import RhinoObject
from compas_fofin.objects import CircleConstraintObject


class RhinoCircleConstraintObject(RhinoObject, CircleConstraintObject):
    """
    Class for interacting with COMPAS circles in Rhino.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoCircleConstraintObject, self).__init__(*args, **kwargs)

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self._guids = self.artist.draw()
