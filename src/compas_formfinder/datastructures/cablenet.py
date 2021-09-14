from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Network


__all__ = ['Cablenet']


class Cablenet(Network):
    """A data structure for cablenets.

    Attributes
    ----------
    default_node_attributes : dict
        The default attributes of all nodes of the cablenet.

        * ``is_anchor (bool)``: Indicates whether a node is anchored and can take reaction forces. Default is ``False``.
        * ``px (float)``: Component along the X axis of an applied point load. Default is ``0.0``.
        * ``py (float)``: Component along the Y axis of an applied point load. Default is ``0.0``.
        * ``pz (float)``: Component along the Z axis of an applied point load. Default is ``0.0``.
        * ``_rx (float)``: Component along the X axis of a residual force. Default is ``0.0``.
        * ``_ry (float)``: Component along the Y axis of a residual force. Default is ``0.0``.
        * ``_rz (float)``: Component along the Z axis of a residual force. Default is ``0.0``.
    """

    def __init__(self):
        super(Cablenet, self).__init__()
        self.default_node_attributes.update({
            'is_anchor': False,
            'px': 0.0,
            'py': 0.0,
            'pz': 0.0,
            '_rx': 0.0,
            '_ry': 0.0,
            '_rz': 0.0
        })
        self.default_edge_attributes.update({
            'q': 1.0,
            'f': None,
            'l': None,
            'l0': None,
            'E': None,
            'radius': None
        })
