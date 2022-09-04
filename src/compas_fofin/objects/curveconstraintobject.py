from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .constraintobject import ConstraintObject


class CurveConstraintObject(ConstraintObject):

    SETTINGS = {}

    def __init__(self, *args, **kwargs):
        super(CurveConstraintObject, self).__init__(*args, **kwargs)

    @property
    def curve(self):
        return self.constraint.geometry
