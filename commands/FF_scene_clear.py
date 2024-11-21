#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.session import FoFinSession


def RunCommand():
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
    RunCommand()