from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_ui.objects import Object
from compas_ui.values import Settings


class CircleConstraintObject(Object):
    SETTINGS = Settings()

    def __init__(self, *args, **kwargs):
        super(CircleConstraintObject, self).__init__(*args, **kwargs)

    @property
    def circle(self):
        return self.constraint.geometry
