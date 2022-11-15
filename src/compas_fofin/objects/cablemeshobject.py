from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from compas_ui.objects import MeshObject
from compas_ui.values import Settings
from compas_ui.values import BoolValue
from compas_ui.values import FloatValue
from compas_ui.values import ColorValue
from compas_ui.values import StrValue


class CableMeshObject(MeshObject):
    """Base object for representing a cable mesh in a scene."""

    # TODO: Move this to a settings object
    # TODO: For every setting use a setting object

    SETTINGS = Settings(
        {
            "layer": StrValue("FF"),
            "show.vertices:free": BoolValue(False),
            "show.vertices:is_anchor": BoolValue(True),
            "show.edges": BoolValue(True),
            "show.faces": BoolValue(False),
            "show.faces:all": BoolValue(False),
            "show.reactions": BoolValue(True),
            "show.loads": BoolValue(True),
            "show.selfweight": BoolValue(True),
            "show.pipes:forcedensities": BoolValue(False),
            "show.pipes:forces": BoolValue(True),
            "show.constraints": BoolValue(True),
            "color.vertices": ColorValue(Color.black()),
            "color.vertices:is_anchor": ColorValue(Color.red()),
            "color.vertices:is_fixed": ColorValue(Color.blue()),
            "color.vertices:is_constrained": ColorValue(Color.cyan()),
            "color.edges": ColorValue(Color.black()),
            "color.faces": ColorValue(Color.white().darkened(25)),
            "color.tension": ColorValue(Color.red()),
            "color.compression": ColorValue(Color.blue()),
            "color.reactions": ColorValue(Color.green().darkened(50)),
            "color.loads": ColorValue(Color.green().darkened(50)),
            "color.selfweight": ColorValue(Color.white()),
            "color.invalid": ColorValue(Color.black()),
            "color.pipes": ColorValue(Color.white().darkened(50)),
            "scale.reactions": FloatValue(0.300),
            "scale.loads": FloatValue(1.0),
            "scale.selfweight": FloatValue(1.0),
            "pipe_thickness.min": FloatValue(0.0),
            "pipe_thickness.max": FloatValue(10.0),
            "tol.externalforces": FloatValue(1e-3),
        }
    )

    def __init__(self, *args, **kwargs):
        super(CableMeshObject, self).__init__(*args, **kwargs)
        self._is_valid = False
        self._group_free = None
        self._group_fixed = None
        self._group_anchors = None
        self._group_edges = None
        self._group_faces = None

    @property
    def layer(self):
        return self.settings.get("layer")

    @layer.setter
    def layer(self, value):
        self.settings["layer"] = value

    @property
    def is_valid(self):
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value):
        self._is_valid = value
        self.settings["show.edges"] = False if self._is_valid else True

    @property
    def show_edges(self):
        if not self.is_valid:
            return True
        return self.settings["show.edges"]

    @show_edges.setter
    def show_edges(self, value):
        self.settings["show.edges"] = bool(value)
