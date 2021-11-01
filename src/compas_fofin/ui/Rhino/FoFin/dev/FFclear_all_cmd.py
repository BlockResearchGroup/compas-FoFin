from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFclear_all"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options = ["Yes", "No"]
    option = compas_rhino.rs.GetString("Clear all FF objects?", strings=options, defaultString="No")
    if not option:
        return

    if option == "Yes":
        scene.clear()
        sc.doc.Views.Redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
