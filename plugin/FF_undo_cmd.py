#! python3
import pathlib

from compas_fofin.session import Session

__commandname__ = "FF_undo"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FormFinder")

    # session.undo()

    # if Rhino file is saved, use parent/.FormFinder/temp/timestamp
    # otherwise use tmp/.FormFinder/temp/timestamp


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
