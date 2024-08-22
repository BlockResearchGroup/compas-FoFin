#! python3
import rhinoscriptsyntax as rs  # type: ignore

from compas.scene import Scene
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")
    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)

    if not meshobj:
        return

    # =============================================================================
    # Move anchors
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    option = rs.GetString(message="Set Direction.", strings=options)
    if not option:
        return

    vertices = meshobj.select_vertices()
    if vertices:
        if option == "Free":
            meshobj.move_vertices(vertices)
        else:
            meshobj.move_vertices_direction(vertices, direction=option)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_anchors = True
    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave"]:
        session.record(eventname="Move Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
