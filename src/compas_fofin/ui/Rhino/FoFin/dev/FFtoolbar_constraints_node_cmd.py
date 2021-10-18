from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFconstraints_node_direction_cmd
import FFconstraints_node_line_cmd
import FFconstraints_node_plane_cmd


__commandname__ = "FFtoolbar_constraints_node"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["Direction", "Line", "Plane"]
    option = compas_rhino.rs.GetString("Select node constraints:", strings=options)

    if not option:
        return

    if option == "Direction":
        FFconstraints_node_direction_cmd.RunCommand(True)

    elif option == "Line":
        FFconstraints_node_line_cmd.RunCommand(True)

    elif option == "Plane":
        FFconstraints_node_plane_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
