from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from compas_ui.objects import MeshObject


class CableMeshObject(MeshObject):
    """Base object for representing a cable mesh in a scene."""

    # TODO: Move this to a settings object
    # TODO: For every setting use a setting object

    SETTINGS = {
        "layer": "FF",
        "show.vertices:free": False,
        "show.vertices:is_anchor": True,
        "show.edges": True,
        "show.faces": False,
        "show.faces:all": False,
        "show.reactions": True,
        "show.loads": True,
        "show.selfweight": True,
        "show.pipes:forcedensities": False,
        "show.pipes:forces": True,
        "show.constraints": True,
        "color.vertices": Color.white(),
        "color.vertices:is_anchor": Color.red(),
        "color.vertices:is_fixed": Color.blue(),
        "color.vertices:is_constrained": Color.cyan(),
        "color.edges": Color.black(),
        "color.faces": Color.white().darkened(25),
        "color.tension": Color.red(),
        "color.compression": Color.blue(),
        "color.reactions": Color.green().darkened(50),
        "color.loads": Color.green().darkened(50),
        "color.selfweight": Color.white(),
        "color.invalid": Color.black(),
        "color.pipes": Color.white().darkened(50),
        "scale.reactions": 0.300,
        "scale.loads": 1.0,
        "scale.selfweight": 1.0,
        "pipe_thickness.min": 0.0,
        "pipe_thickness.max": 10.0,
        "tol.externalforces": 1e-3,
    }

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
