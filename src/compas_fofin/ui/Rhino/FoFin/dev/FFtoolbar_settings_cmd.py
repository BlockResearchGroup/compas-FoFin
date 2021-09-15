from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFsettings_cmd


__commandname__ = "FFtoolbar_settings"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    FFsettings_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
