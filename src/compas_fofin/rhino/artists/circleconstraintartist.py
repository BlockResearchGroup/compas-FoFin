from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color

from compas_rhino.artists import RhinoArtist
from compas_fofin.artists import ConstraintArtist


class RhinoCircleConstraintArtist(RhinoArtist, ConstraintArtist):
    """Artist for drawing circle constraints.

    Parameters
    ----------
    circleconstraint : :class:`~compas_fd.constraints.CircleConstraint`
        A COMPAS circle constraint.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ConstraintArtist`.

    """

    def __init__(self, circleconstraint, layer=None, **kwargs):
        super(RhinoCircleConstraintArtist, self).__init__(
            constraint=circleconstraint,
            layer=layer,
            **kwargs,
        )

    def draw(self, color=None):
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the circle.
            Default is :attr:`compas_fofin.artists.ConstraintArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        circles = [
            {
                "plane": self.constraint.geometry.plane,
                "radius": self.constraint.geometry.radius,
                "color": color.rgb255,
                "name": self.constraint.geometry.name,
            }
        ]
        return compas_rhino.draw_circles(
            circles,
            layer=self.layer,
            clear=False,
            redraw=False,
        )
