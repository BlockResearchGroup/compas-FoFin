#! python3
import pathlib

from compas_fofin.session import Session

__commandname__ = "FF_open"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FormFinder")

    # session.open(...)

    # ask for filepath to existing session
    # use parent of currentRhino file, if it exsists, as starting point


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
