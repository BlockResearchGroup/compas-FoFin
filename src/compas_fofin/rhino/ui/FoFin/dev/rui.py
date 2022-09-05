import os
from compas_ui.rhino.rui import Rui

HERE = os.path.dirname(__file__)
UIPATH = os.path.join(HERE, "ui.json")
RUIPATH = os.path.join(HERE, "FOFIN.rui")

rui = Rui.from_json(UIPATH, RUIPATH)

rui.write()
