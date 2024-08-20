#! python3
from compas.scene import Scene
from compas_fofin.session import Session

__commandname__ = "FF_clear"


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Get stuff from session
    # =============================================================================

    scene: Scene = session.setdefault("scene", factory=Scene)
    scene.clear()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
