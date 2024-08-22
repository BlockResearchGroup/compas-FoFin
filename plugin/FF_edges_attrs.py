#! python3
from compas.scene import Scene
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")
    scene: Scene = session.setdefault("scene", factory=Scene)

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    edges = meshobj.select_edges()
    if edges:
        meshobj.update_edge_attributes(edges=edges)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
