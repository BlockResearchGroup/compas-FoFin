from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.ui import CommandMenu
from compas_ui.app import App


__commandname__ = "FF_cloud_shutdown"


@App.error()
def RunCommand(is_interactive):

    app = App()

    config = {
        "name": "Cloud",
        "message": "Shutdown server?",
        "options": [
            {
                "name": "Yes",
                "message": "Yes",
                "action": None
            },
            {
                "name": "No",
                "message": "No",
                "action": None
            }
        ]
    }

    menu = CommandMenu(config)
    action = menu.select_action()

    if action['name'] == 'Yes':
        app.proxy.shutdown()


if __name__ == "__main__":
    RunCommand(True)
