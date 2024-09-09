#! python3
import rhinoscriptsyntax as rs  # type: ignore

import compas_fofin.settings
from compas_fofin.scene import RhinoCableMeshObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()
    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")

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

    meshobj.show_vertices = True
    meshobj.show_free = False
    meshobj.show_supports = True

    rs.EnableRedraw(False)
    meshobj.clear_vertices()
    meshobj.draw_vertices()
    rs.EnableRedraw(True)
    rs.Redraw()

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

    meshobj.show_vertices = True
    meshobj.show_supports = True
    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(eventname="Move Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
