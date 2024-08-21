#! python3
import rhinoscriptsyntax as rs  # type: ignore

from compas.scene import Scene
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")
    scene: Scene = session.setdefault("scene", factory=Scene)

    result = rs.MessageBox(
        "Note that this will remove all FormFinder data and objects. Do you wish to proceed?",
        buttons=4 | 32 | 256 | 0,
        title="Clear FormFinder",
    )

    if result == 6:
        scene.clear()

        if session.CONFIG["autosave"]:
            session.record(eventname="Clear")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)