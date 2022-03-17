from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from compas_ui.objects import MeshObject


class CableMeshObject(MeshObject):
    """Base object for representing a cable mesh in a scene.
    """

    SETTINGS = {
        '_is.valid': False,

        'layer': "FF::CableMesh",

        'show.vertices:is_anchor': True,
        'show.vertices:free': False,
        'show.edges': True,
        'show.faces': False,
        'show.faces:all': False,
        'show.reactions': True,
        'show.loads': True,
        'show.pipes:forcedensities': False,
        'show.pipes:forces': False,

        'color.vertices': Color.white(),
        'color.vertices:is_anchor': Color.red(),
        'color.vertices:is_fixed': Color.blue(),
        'color.vertices:is_constrained': Color.cyan(),
        'color.edges': Color.black(),
        'color.edges:tension': Color.red(),
        'color.edges:compression': Color.blue(),
        'color.faces': Color.white().darkened(25),
        'color.reactions': Color.green().darkened(50),
        'color.loads': Color.green().darkened(75),
        'color.invalid': Color.magenta(),
        'color.pipes': Color.white().darkened(50),

        'scale.externalforces': 1,
        'pipe_thickness.min': 0,
        'pipe_thickness.max': 10,
        'tol.externalforces': 1e-3,
    }

    def __init__(self, *args, **kwargs):
        super(CableMeshObject, self).__init__(*args, **kwargs)
