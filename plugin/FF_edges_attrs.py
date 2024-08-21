#! python3
from compas.scene import Scene
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")
    scene: Scene = session.setdefault("scene", factory=Scene)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
