from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino

from compas_cloud import Proxy  # noqa: E402
from compas_fofin.scene import Scene  # noqa: E402
from compas_fofin.rhino import FF_error  # noqa: E402
from compas_fofin.activate import check
from compas_fofin.activate import activate
from compas_fofin.rhino import Browser
from compas_fofin.session import Session

__commandname__ = "FFinit"


SETTINGS = {

    "FF": {
    },

    "Solvers": {
    }
}


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

    errorHandler = FF_error(title="Server side Error", showLocalTraceback=False)
    proxy = Proxy(errorHandler=errorHandler, port=9009)

    scene = Scene(SETTINGS)
    scene.clear()

    Session(directory=CWD, extension='FF', proxy=proxy, scene=scene)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
