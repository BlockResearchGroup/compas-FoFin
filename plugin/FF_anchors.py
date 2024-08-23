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
    # Preselect anchors
    # =============================================================================

    fixed = list(mesh.vertices_where(is_fixed=True))
    leaves = list(mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        mesh.vertices_attribute("is_anchor", True, keys=vertices)

    # =============================================================================
    # Select/Unselect anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Anchors", strings=["Add", "Remove"])
    if not option:
        return

    if option == "Add":

        vertices = meshobj.select_vertices(show_anchors=True, show_free=True)
        if vertices:
            mesh.vertices_attribute("is_anchor", True, keys=vertices)

    elif option == "Remove":

        vertices = meshobj.select_vertices(show_anchors=True, show_free=False)
        if vertices:
            mesh.vertices_attribute("is_anchor", False, keys=vertices)
            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

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
        session.record(eventname="Add/Remove Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
