#! python3
# venv: brg-csd
# r: compas_fofin>=0.14.0

from compas_fofin.session import FoFinSession
from compas_rui.forms import FileForm


def RunCommand():
    session = FoFinSession()

    filepath = FileForm.save(session.basedir, "FormFinder.json")
    if not filepath:
        return

    session.dump(filepath)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
