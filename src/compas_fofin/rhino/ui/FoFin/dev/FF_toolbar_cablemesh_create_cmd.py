from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.ui import UI

import FF_cablemesh_from_meshgrid_cmd
import FF_cablemesh_from_mesh_cmd
import FF_cablemesh_from_box_cmd
import FF_cablemesh_from_cylinder_cmd
import FF_cablemesh_from_surface_cmd


__commandname__ = "FF_toolbar_cablemesh_create"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()  # noqa: F841

    options = ["FromMeshgrid", "FromMesh", "FromSurface", "FromBox", "FromCylinder"]
    option = compas_rhino.rs.GetString("Create Cablemesh", strings=options)

    if not option:
        return

    if option == "FromMeshgrid":
        FF_cablemesh_from_meshgrid_cmd.RunCommand(True)

    elif option == "FromMesh":
        FF_cablemesh_from_mesh_cmd.RunCommand(True)

    elif option == "FromSurface":
        FF_cablemesh_from_surface_cmd.RunCommand(True)

    elif option == "FromBox":
        FF_cablemesh_from_box_cmd.RunCommand(True)

    elif option == "FromCylinder":
        FF_cablemesh_from_cylinder_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
