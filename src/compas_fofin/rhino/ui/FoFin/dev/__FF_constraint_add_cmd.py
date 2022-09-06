from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
from compas_rhino.geometry import RhinoSurface

from compas_ui.ui import UI
from compas_fd.constraints import Constraint


__commandname__ = "FF_constraint_add"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    ctypes = ["Line", "Curve", "Surface"]
    ctype = ui.get_string("Node constraint type?", options=ctypes)
    if not ctype:
        return

    if ctype == "Line":
        guid = compas_rhino.select_line(message="Select line constraint")
        if not guid:
            return

        # ask for a name?
        # add to a group? => constraints...

        line = RhinoLine.from_guid(guid).to_compas()
        constraint = Constraint(line)
        constraint.name = "LineConstraint"

        compas_rhino.rs.HideObject(guid)
        ui.scene.add(constraint, name=constraint.name)

    elif ctype == "Curve":
        guid = compas_rhino.select_curve(message="Select curve constraint")
        if not guid:
            return

        # ask for a name?
        # add to a group? => constraints...

        curve = RhinoCurve.from_guid(guid).to_compas()
        constraint = Constraint(curve)
        constraint.name = "CurveConstraint"

        compas_rhino.rs.HideObject(guid)
        ui.scene.add(constraint, name=constraint.name)

    elif ctype == "Surface":
        guid = compas_rhino.select_surface(message="Select surface constraint")
        if not guid:
            return

        surface = RhinoSurface.from_guid(guid).to_compas()
        constraint = Constraint(surface)

        raise NotImplementedError

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
