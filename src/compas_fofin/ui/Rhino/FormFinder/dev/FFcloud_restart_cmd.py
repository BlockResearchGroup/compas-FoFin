from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.ui import CommandMenu
from compas_fofin.rhino import get_proxy


__commandname__ = "FFcloud_restart"


def RunCommand(is_interactive):

    config = {
        "name": "Cloud",
        "message": "start cloud in ?",
        "options": [
            {
                "name": "background",
                "message": "background",
                "action": None
            },
            {
                "name": "console",
                "message": "console",
                "action": None
            }
        ]
    }

    menu = CommandMenu(config)
    action = menu.select_action()

    if action['name'] == 'background':
        background = True
    if action['name'] == 'console':
        background = False

    p = get_proxy()
    p.background = background
    p.restart()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
