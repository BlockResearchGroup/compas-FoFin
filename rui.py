import json
import pathlib
import zipfile

from compas_rui.rui import Rui

HERE = pathlib.Path(__file__).parent.absolute()

UI = HERE / "compas-FoFin.json"
RHPROJ = HERE / "compas-FoFin.rhproj"
RUI = HERE / "COMPAS-FoFin.rui"
BUILD = HERE / "build/rh8"
YAK = [path for path in BUILD.iterdir() if path.suffix == ".yak"][0]

with open(RHPROJ, mode="rt") as f:
    rhproj = json.load(f)
    guid = rhproj["id"]

rui = Rui.from_json(UI, RUI, guid=guid)
rui.write()

with zipfile.ZipFile(YAK, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write(RUI, "COMPAS-FoFin.rui")