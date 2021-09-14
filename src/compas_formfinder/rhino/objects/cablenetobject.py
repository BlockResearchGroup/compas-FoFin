from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from compas.geometry import Point
# from compas.geometry import Scale
# from compas.geometry import Translation
# from compas.geometry import Rotation
# from compas.utilities import i_to_rgb
# import compas_rhino

from .meshobject import MeshObject


__all__ = ["CablenetObject"]


class CablenetObject(MeshObject):
    """Scene object for FF CableNet.
    """

    SETTINGS = {
        'layer': "FF::Cablenet",
        'show.vertices': True,
        'show.edges': True,
        'color.vertices': [0, 255, 255],
        'color.vertices:is_fixed': [0, 255, 255],
        'color.edges': [0, 0, 255],
        'color.tension': [255, 0, 0]
    }
