from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.ui import CommandMenu
from compas_ui.app import App


__commandname__ = "FF_cloud_restart"


@App.error()
def RunCommand(is_interactive):

    app = App()

    config = {
        "name": "Cloud",
        "message": "Mode?",
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

    app.proxy.background = action['name'] == 'background'
    app.proxy.restart()


if __name__ == "__main__":
    RunCommand(True)
