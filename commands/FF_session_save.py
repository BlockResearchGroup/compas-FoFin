#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

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
