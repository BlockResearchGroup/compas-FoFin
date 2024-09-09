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

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    # =============================================================================
    # Update attributes
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_edges = True

    rs.EnableRedraw(False)
    meshobj.clear_edges()
    meshobj.draw_edges()
    rs.EnableRedraw(True)
    rs.Redraw()

    edges = meshobj.select_edges()

    if edges:
        meshobj.update_edge_attributes(edges=edges)

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
        session.record(eventname="Edges Attributes")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
