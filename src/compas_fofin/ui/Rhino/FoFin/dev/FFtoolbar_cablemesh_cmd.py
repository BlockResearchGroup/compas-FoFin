from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFcablemesh_from_mesh_cmd
import FFcablemesh_from_meshgrid_cmd
import FFcablemesh_from_box_cmd
import FFcablemesh_from_cylinder_cmd


__commandname__ = "FFtoolbar_cablemesh"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options = ["Mesh", "Meshgrid", "Box", "Cylinder"]
    option = compas_rhino.rs.GetString("Create CableMesh:", strings=options)

    if not option or option is None:
        scene.update()
        return
    option = option.lower()

    if option == "mesh":
        FFcablemesh_from_mesh_cmd.RunCommand(True)

    elif option == "meshgrid":
        FFcablemesh_from_meshgrid_cmd.RunCommand(True)

    elif option == "box":
        FFcablemesh_from_box_cmd.RunCommand(True)

    elif option == "cylinder":
        FFcablemesh_from_cylinder_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
