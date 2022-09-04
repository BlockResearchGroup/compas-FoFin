from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid
from compas_ui.objects import Object


class ConstraintObject(Object):

    SETTINGS = {}

    def __init__(self, *args, **kwargs):
        super(ConstraintObject, self).__init__(*args, **kwargs)

    @property
    def state(self):
        return {
            "guid": str(self.guid),
            "name": self.name,
            "item": str(self.item.guid),
            "parent": str(self.parent.guid) if self.parent else None,
            "settings": self.settings,
            "artist": self.artist.state,
            "visible": self.visible,
        }

    @state.setter
    def state(self, state):
        self._guid = uuid.UUID(state["guid"])
        self.name = state["name"]
        self.settings.update(state["settings"])
        self.artist.state = state["artists"]
        self.visible = state["visible"]

    @property
    def constraint(self):
        return self.item

    @constraint.setter
    def constraint(self, constraint):
        self.item = constraint

    def move(self):
        raise NotImplementedError
