from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color

from compas_rhino.artists import RhinoArtist
from compas_fofin.artists import ConstraintArtist


class RhinoLineConstraintArtist(RhinoArtist, ConstraintArtist):
    """Artist for drawing line constraints.

    Parameters
    ----------
    lineconstraint : :class:`~compas_fd.constraints.LineConstraint`
        A COMPAS line constraint.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ConstraintArtist`.

    """

    def __init__(self, lineconstraint, layer=None, **kwargs):
        super(RhinoLineConstraintArtist, self).__init__(
            constraint=lineconstraint,
            layer=layer,
            **kwargs,
        )

    def draw(self, color=None, show_points=False):
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the line.
            Default is :attr:`compas_fofin.artists.ConstraintArtist.color`.
        show_points : bool, optional
            If True, draw the start and end point of the line constraint.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        start = list(self.constraint.geometry.start)
        end = list(self.constraint.geometry.end)
        color = Color.coerce(color) or self.color
        color = color.rgb255

        guids = []

        if show_points:
            # points = [
            #     {"pos": start, "color": color, "name": self.constraint.geometry.name},
            #     {"pos": end, "color": color, "name": self.constraint.geometry.name},
            # ]
            # guids += compas_rhino.draw_points(
            #     points,
            #     layer=self.layer,
            #     clear=False,
            #     redraw=False,
            # )
            raise NotImplementedError

        lines = [
            {
                "start": start,
                "end": end,
                "color": color,
                "name": self.constraint.geometry.name,
            }
        ]

        guids += compas_rhino.draw_lines(
            lines,
            layer=self.layer,
            clear=False,
            redraw=False,
        )
        return guids
