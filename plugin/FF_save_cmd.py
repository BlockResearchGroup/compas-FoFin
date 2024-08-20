#! python3
from compas_fofin.rhino.forms.filesystem import FileForm
from compas_fofin.session import Session

__commandname__ = "FF_save"


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    filepath = FileForm.save(session.basedir, "FormFinder.json")
    if not filepath:
        return

    session.save(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
