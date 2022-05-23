import os
from compas_ui.rhino.rui import Rui

HERE = os.path.dirname(__file__)
CONFIGPATH = os.path.join(HERE, "config.json")
RUIPATH = os.path.join(HERE, "FOFIN.rui")

rui = Rui.from_json(CONFIGPATH, RUIPATH)

rui.write()
