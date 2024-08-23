#! python3
import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Delete edges
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Update ForceDensity", strings=["Value", "ScaleFactor"])
    if not option:
        return

    meshobj.show_edges = True
    edges = meshobj.select_edges()

    if edges:

        if option == "Value":
            value = rs.GetReal(message="Value")
            mesh.edges_attribute("q", value, keys=edges)

        elif option == "ScaleFactor":
            factor = rs.GetReal(message="ScaleFactor")

            for edge in edges:
                q = mesh.edge_attribute(edge, "q")
                mesh.edge_attribute(edge, "q", q * factor)

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

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Delete Edges")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
