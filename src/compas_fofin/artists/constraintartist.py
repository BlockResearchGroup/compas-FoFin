from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from compas.artists import Artist


class ConstraintArtist(Artist):
    """Base class for artists for constraints.

    Parameters
    ----------
    constraint : :class:`~compas_fd.constraints.Constraint`
        The constraint.
    color : tuple[float, float, float] | :class:`~compas.colors.Color`, optional
        The RGB components of the base color of the constraint.

    Attributes
    ----------
    constraint : :class:`~compas_fd.constraints.Constraint`
        The constraint associated with the artist.
    color : :class:`~compas.colors.Color`
        The color of the object.

    Class Attributes
    ----------------
    default_color : :class:`~compas.colors.Color`
        The default rgb color value of the constraint.

    """

    default_color = Color.from_hex("#0092D2")

    def __init__(self, constraint, color=None, **kwargs):
        super(ConstraintArtist, self).__init__()
        self._constraint = None
        self._default_color = None
        self._color = None

        self.constraint = constraint
        self.color = color

    @property
    def state(self):
        return {
            "default_color": self.default_color,
            "color": self.color,
        }

    @state.setter
    def state(self, state):
        self.default_color = state["default_color"]
        self.color = state["color"]

    @property
    def constraint(self):
        return self._constraint

    @constraint.setter
    def constraint(self, constraint):
        self._constraint = constraint

    @property
    def color(self):
        if not self._color:
            self.color = self.default_color
        return self._color

    @color.setter
    def color(self, value):
        self._color = Color.coerce(value)
