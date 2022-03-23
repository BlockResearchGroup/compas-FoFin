from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.app import App

import FF_cablemesh_from_meshgrid_cmd
import FF_cablemesh_from_mesh_cmd
import FF_cablemesh_from_box_cmd
import FF_cablemesh_from_cylinder_cmd


__commandname__ = 'FF_toolbar_cablemesh_create'


@App.error()
def RunCommand(is_interactive):

    options = ["FromMeshgrid", 'FromMesh', "FromBox", "FromCylinder"]
    option = compas_rhino.rs.GetString("Create Cablemesh:", strings=options)

    if not option:
        return

    if option == "FromMeshgrid":
        FF_cablemesh_from_meshgrid_cmd.RunCommand(True)

    elif option == "FromMesh":
        FF_cablemesh_from_mesh_cmd.RunCommand(True)

    elif option == "FromBox":
        FF_cablemesh_from_box_cmd.RunCommand(True)

    elif option == "FromCylinder":
        FF_cablemesh_from_cylinder_cmd.RunCommand(True)


if __name__ == '__main__':
    RunCommand(True)
