from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.app import App

import FF_save_cmd
import FF_saveas_cmd
import FF_cablemesh_data_save_cmd


__commandname__ = 'FF_toolbar_save'


@App.error()
def RunCommand(is_interactive):

    options = ["SaveSession", "SaveSessionAs", "SaveMeshData"]
    option = compas_rhino.rs.GetString("Create Cablemesh:", strings=options)

    if not option:
        return

    if option == "SaveSession":
        FF_save_cmd.RunCommand(True)

    elif option == "SaveSessionAs":
        FF_saveas_cmd.RunCommand(True)

    elif option == "SaveMeshData":
        FF_cablemesh_data_save_cmd.RunCommand(True)


if __name__ == '__main__':
    RunCommand(True)
