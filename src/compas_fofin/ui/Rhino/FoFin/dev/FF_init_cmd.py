import os
import json
from compas_ui.ui import UI


__commandname__ = "FF_init"

HERE = os.path.dirname(__file__)
SPLASH = os.path.join(HERE, "assets", "index.html")

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)


@UI.error()
def RunCommand(is_interactive):

    UI.reset()
    ui = UI(config=CONFIG)
    ui.splash(url=SPLASH)
    ui.scene_clear()


if __name__ == '__main__':
    RunCommand(True)
