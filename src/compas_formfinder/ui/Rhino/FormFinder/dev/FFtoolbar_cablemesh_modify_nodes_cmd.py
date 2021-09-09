from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_formfinder.rhino import get_scene
from compas_formfinder.rhino import FF_error

import FFcablemesh_anchors_cmd
import FFcablemesh_move_nodes_cmd
import FFcablemesh_modify_nodes_cmd


__commandname__ = "FFtoolbar_cablemesh_modify_nodes"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["IdentifyAnchors", "MoveNodes", "NodesAttributes"]
    option = compas_rhino.rs.GetString("Modify CableMesh nodes:", strings=options)

    if not option:
        return

    if option == "IdentifyAnchors":
        FFcablemesh_anchors_cmd.RunCommand(True)

    elif option == "MoveNodes":
        FFcablemesh_move_nodes_cmd.RunCommand(True)

    elif option == "NodesAttributes":
        FFcablemesh_modify_nodes_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)