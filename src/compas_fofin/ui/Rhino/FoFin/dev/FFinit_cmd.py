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
from compas_ui.app import App

__commandname__ = "FFinit"


HERE = os.path.dirname(__file__)

compas.PRECISION = '3f'


@FF_error()
def RunCommand(is_interactive):

    # if check():
    #     print("Current plugin is already activated")
    # else:
    #     compas_rhino.rs.MessageBox("Detected environment change, re-activating plugin", 0, "Re-activating Needed")
    #     if activate():
    #         compas_rhino.rs.MessageBox("Restart Rhino for the change to take effect", 0, "Restart Rhino")
    #     else:
    #         compas_rhino.rs.MessageBox("Someting wrong during re-activation", 0, "Error")
    #     return

    Browser()

    config = compas.json_load(os.path.join(HERE, 'config.json'))
    App(name='fofin', settings=config['settings'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
