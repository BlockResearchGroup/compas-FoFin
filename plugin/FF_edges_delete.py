#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import rhinoscriptsyntax as rs  # type: ignore

import compas_fofin.settings
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

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

    rs.EnableRedraw(False)
    meshobj.clear_edges()
    meshobj.draw_edges()
    rs.EnableRedraw(True)
    rs.Redraw()

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
        session.record(name="Delete Edges")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
