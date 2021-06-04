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


__all__ = ["CableMeshObject"]


class CableMeshObject(MeshObject):
    """Scene object for FF cable meshes.
    """

    SETTINGS = {
        'layer': "FF::CableMesh",
        'show.vertices': True,
        'show.edges': True,
        'show.faces': True,
        'color.vertices': [255, 255, 255],
        'color.vertices:is_anchor': [255, 0, 0],
        'color.vertices:is_fixed': [0, 0, 255],
        'color.vertices:is_constrained': [0, 255, 255],
        'color.edges': [0, 0, 255],
        'color.tension': [255, 0, 0],
        'color.faces': [200, 200, 200]
    }
