from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_ui.objects import Object


class LineConstraintObject(Object):

    SETTINGS = {}

    def __init__(self, *args, **kwargs):
        super(LineConstraintObject, self).__init__(*args, **kwargs)

    @property
    def line(self):
        return self.constraint.geometry

    def move_start(self):
        raise NotImplementedError

    def move_end(self):
        raise NotImplementedError
