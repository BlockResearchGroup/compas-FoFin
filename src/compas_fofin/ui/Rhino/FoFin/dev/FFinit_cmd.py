from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino

from compas_fofin.rhino import FF_error
from compas_fofin.activate import check
from compas_fofin.activate import activate
from compas_fofin.rhino import Browser
from compas_fofin.app import App

__commandname__ = "FFinit"


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME

compas.PRECISION = '3f'


@FF_error()
def RunCommand(is_interactive):

    if check():
        print("Current plugin is already activated")
    else:
        compas_rhino.rs.MessageBox("Detected environment change, re-activating plugin", 0, "Re-activating Needed")
        if activate():
            compas_rhino.rs.MessageBox("Restart Rhino for the change to take effect", 0, "Restart Rhino")
        else:
            compas_rhino.rs.MessageBox("Someting wrong during re-activation", 0, "Error")
        return

    Browser()
    App()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
