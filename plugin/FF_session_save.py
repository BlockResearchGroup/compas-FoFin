#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

from compas_fofin.session import FoFinSession
from compas_rui.forms import FileForm


def RunCommand(is_interactive):
    session = FoFinSession()

    filepath = FileForm.save(session.basedir, "FormFinder.json")
    if not filepath:
        return

    session.dump(filepath)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
