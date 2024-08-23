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

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)

    if not meshobj:
        return

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Delete edges
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_edges = True
    edges = meshobj.select_edges()

    if edges:
        faces = set()
        for edge in edges:
            faces.update(mesh.edge_faces(edge))

        for face in faces:
            if face is not None:
                if mesh.has_face(face):
                    mesh.delete_face(face)

        mesh.remove_unused_vertices()

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
