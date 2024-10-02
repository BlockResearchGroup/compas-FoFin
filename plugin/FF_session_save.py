#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

from compas_rui.forms import FileForm
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

    filepath = FileForm.save(session.basedir, "FormFinder.json")
    if not filepath:
        return

    session.save(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
