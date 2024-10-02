#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_fofin.settings
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_rui.forms import SettingsForm
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")
    scene = session.scene()

    mesh: RhinoCableMeshObject = scene.find_by_itemtype(itemtype=CableMesh)

    if mesh:
        if "CableMesh" in compas_fofin.settings.SETTINGS:
            for key, value in compas_fofin.settings.SETTINGS["CablMesh"].items():
                name = "_".join(key.split("."))
                if hasattr(mesh, name):
                    value.set(getattr(mesh, name))

    settingsmesh = SettingsForm(settings=compas_fofin.settings.SETTINGS, use_tab=True)
    if settingsmesh.show():

        if mesh:
            if "CableMesh" in compas_fofin.settings.SETTINGS:
                for key, value in compas_fofin.settings.SETTINGS["CablMesh"].items():
                    name = "_".join(key.split("."))
                    setattr(mesh, name, value.value)

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(name="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
