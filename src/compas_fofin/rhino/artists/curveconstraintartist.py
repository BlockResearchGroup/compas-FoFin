from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color

from compas_rhino.artists import RhinoArtist
from compas_fofin.artists import ConstraintArtist


class RhinoCurveConstraintArtist(RhinoArtist, ConstraintArtist):
    """Artist for drawing curve constraints.

    Parameters
    ----------
    curveconstraint : :class:`~compas_fd.constraints.CurveConstraint`
        A COMPAS curve constraint.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ConstraintArtist`.

    """

    def __init__(self, curveconstraint, layer=None, **kwargs):
        super(RhinoCurveConstraintArtist, self).__init__(
            constraint=curveconstraint,
            layer=layer,
            **kwargs,
        )

    def draw(self, color=None, show_points=False):
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            Default is :attr:`compas_fofin.artists.ConstraintArtist.color`.
        show_points : bool, optional
            If True, draw the control points of the curve.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        curves = [
            {
                "curve": self.constraint.geometry,
                "color": color.rgb255,
                "name": self.constraint.geometry.name,
            }
        ]
        return compas_rhino.draw_curves(
            curves,
            layer=self.layer,
            clear=False,
            redraw=False,
        )
