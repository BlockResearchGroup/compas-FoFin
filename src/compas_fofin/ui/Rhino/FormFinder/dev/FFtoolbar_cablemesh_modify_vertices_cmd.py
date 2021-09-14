from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFcablemesh_anchors_cmd
import FFcablemesh_move_vertices_cmd
import FFcablemesh_modify_vertices_cmd


__commandname__ = "FFtoolbar_cablemesh_modify_vertices"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["IdentifyAnchors", "MoveVertices", "VerticesAttributes"]
    option = compas_rhino.rs.GetString("Modify CableMesh vertices:", strings=options)

    if not option:
        return

    if option == "IdentifyAnchors":
        FFcablemesh_anchors_cmd.RunCommand(True)

    elif option == "MoveVertices":
        FFcablemesh_move_vertices_cmd.RunCommand(True)

    elif option == "VerticesAttributes":
        FFcablemesh_modify_vertices_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
