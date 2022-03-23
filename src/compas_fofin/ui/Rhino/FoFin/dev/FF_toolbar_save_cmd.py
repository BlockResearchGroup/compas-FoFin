from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.app import App

import FF_save_cmd
import FF_saveas_cmd
import FF_save_data_cmd


__commandname__ = 'FF_settings'


@App.error()
def RunCommand(is_interactive):

    app = App()

    options = ["Save", 'SaveAs', "SaveData"]
    option = compas_rhino.rs.GetString("Create Cablemesh:", strings=options)

    if not option:
        return

    if option == "Save":
        FF_save_cmd.RunCommand(True)

    elif option == "SaveAs":
        FF_saveas_cmd.RunCommand(True)

    elif option == "SaveData":
        FF_save_data_cmd.RunCommand(True)


if __name__ == '__main__':
    RunCommand(True)
