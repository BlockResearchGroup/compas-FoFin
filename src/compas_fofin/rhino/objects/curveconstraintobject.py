from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import compas_rhino

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_ui.rhino.objects import RhinoObject
from compas_fofin.objects import CurveConstraintObject


class RhinoCurveConstraintObject(RhinoObject, CurveConstraintObject):
    """
    Class for interacting with COMPAS curves in Rhino.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoCurveConstraintObject, self).__init__(*args, **kwargs)

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self._guids = self.artist.draw()

    def move_start(self):
        """
        Move the starting point of the curve.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Curve
            from compas_fd.constraints import Constraint
            from compas_ui.objects import Object

            curve = Curve([0, 0, 0], [1, 0, 0])
            constraint = Constraint(curve)

            obj = Object(constraint)
            obj.draw()

            compas_rhino.redraw()

            if obj.move_start():
                obj.clear()
                obj.draw()

        """
        start = point_to_rhino(self.curve.start)
        end = point_to_rhino(self.curve.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedLine(start, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(end, False)
        gp.DrawLineFromPoint(end, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = point_to_compas(gp.Point())
        self.curve.start = start
        return True

    def move_end(self):
        """
        Move the end point of the curve.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Curve
            from compas_fd.constraints import Constraint
            from compas_ui.objects import Object

            curve = Curve([0, 0, 0], [1, 0, 0])
            constraint = Constraint(curve)

            obj = Object(constraint)
            obj.draw()

            compas_rhino.redraw()

            if obj.move_end():
                obj.clear()
                obj.draw()

        """
        start = point_to_rhino(self.curve.start)
        end = point_to_rhino(self.curve.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedLine(end, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = point_to_compas(gp.Point())
        self.curve.end = end
        return True
