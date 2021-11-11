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

    options = ["FromMesh", "FromMeshgrid", "FromBox", "FromCylinder"]
    option = compas_rhino.rs.GetString("Create CableMesh:", strings=options).lower()

    if not option:
        return

    if option == "frommesh":
        FFcablemesh_from_mesh_cmd.RunCommand(True)

    elif option == "frommeshgrid":
        FFcablemesh_from_meshgrid_cmd.RunCommand(True)

    elif option == "frombox":
        FFcablemesh_from_box_cmd.RunCommand(True)

    elif option == "fromcylinder":
        FFcablemesh_from_cylinder_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
