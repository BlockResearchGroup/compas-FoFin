#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import rhinoscriptsyntax as rs  # type: ignore

import compas_fofin.settings
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")
    scene = session.scene()

    result = rs.MessageBox(
        "Note that this will remove all FormFinder data and objects. Do you wish to proceed?",
        buttons=4 | 32 | 256 | 0,
        title="Clear FormFinder",
    )

    if result == 6:
        scene.clear()

        if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
            session.record(name="Clear")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
