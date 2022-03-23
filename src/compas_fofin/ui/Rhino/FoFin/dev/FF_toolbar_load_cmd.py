from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.app import App

import FF_load_cmd
import FF_cablemesh_data_load_cmd


__commandname__ = 'FF_toolbar_load'


@App.error()
def RunCommand(is_interactive):

    options = ["LoadSession", "LoadMeshData"]
    option = compas_rhino.rs.GetString("Create Cablemesh:", strings=options)

    if not option:
        return

    if option == "LoadSession":
        FF_load_cmd.RunCommand(True)

    elif option == "LoadMeshData":
        FF_cablemesh_data_load_cmd.RunCommand(True)


if __name__ == '__main__':
    RunCommand(True)
