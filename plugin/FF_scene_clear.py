#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.session import FoFinSession


def RunCommand(is_interactive):
    session = FoFinSession()

    result = rs.MessageBox(
        "Note that this will remove all FormFinder data and objects. Do you wish to proceed?",
        buttons=4 | 32 | 256 | 0,
        title="Clear FormFinder",
    )

    if result == 6:
        session.clear()

        if session.settings.autosave:
            session.record(name="Clear")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
