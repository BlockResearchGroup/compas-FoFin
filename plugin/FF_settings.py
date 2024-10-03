#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_fofin.settings
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_rui.forms import SettingsForm
from compas_rui.values import BoolValue
from compas_rui.values import FloatValue
from compas_rui.values import Settings
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")
    scene = session.scene()

    SETTINGS = compas_fofin.settings.SETTINGS

    meshobj: RhinoCableMeshObject = scene.find_by_itemtype(itemtype=CableMesh)
    if meshobj:
        SETTINGS["CableMesh"] = Settings(
            {
                # "show_supports": BoolValue(meshobj.show_supports),
                # "show_free": BoolValue(meshobj.show_free),
                "show_forces": BoolValue(meshobj.show_forces),
                "show_residuals": BoolValue(meshobj.show_residuals),
                "show_reactions": BoolValue(meshobj.show_reactions),
                "show_loads": BoolValue(meshobj.show_loads),
                "show_selfweight": BoolValue(meshobj.show_selfweight),
                "scale_forces": FloatValue(meshobj.scale_forces),
                "scale_residuals": FloatValue(meshobj.scale_residuals),
                "scale_loads": FloatValue(meshobj.scale_loads),
                "scale_selfweight": FloatValue(meshobj.scale_selfweight),
            }
        )

    form = SettingsForm(settings=SETTINGS, use_tab=True)

    if form.show():
        if meshobj:
            meshobj.show_forces = SETTINGS["CableMesh"]["show_forces"]
            meshobj.show_residuals = SETTINGS["CableMesh"]["show_residuals"]
            meshobj.show_reactions = SETTINGS["CableMesh"]["show_reactions"]
            meshobj.show_loads = SETTINGS["CableMesh"]["show_loads"]
            meshobj.show_selfweight = SETTINGS["CableMesh"]["show_selfweight"]
            meshobj.scale_forces = SETTINGS["CableMesh"]["scale_forces"]
            meshobj.scale_residuals = SETTINGS["CableMesh"]["scale_residuals"]
            meshobj.scale_loads = SETTINGS["CableMesh"]["scale_loads"]
            meshobj.scale_selfweight = SETTINGS["CableMesh"]["scale_selfweight"]

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(name="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
