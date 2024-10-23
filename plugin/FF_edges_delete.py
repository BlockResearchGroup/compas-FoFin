#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD


def RunCommand(is_interactive):
    session = FoFinSession()

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")
    if not meshobj:
        return

    # =============================================================================
    # Clear conduits
    # =============================================================================

    meshobj.clear_conduits()

    meshobj.display_edges_conduit()
    meshobj.display_mesh_conduit()

    # =============================================================================
    # Delete edges
    # =============================================================================

    rs.UnselectAllObjects()

    selectable = list(meshobj.mesh.edges())
    selected = meshobj.select_edges(selectable)

    if selected:
        faces = set()
        for edge in selected:
            faces.update(meshobj.mesh.edge_faces(edge))

        for face in faces:
            if face is not None:
                if meshobj.mesh.has_face(face):
                    meshobj.mesh.delete_face(face)

        meshobj.mesh.remove_unused_vertices()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.clear()
    meshobj.clear_conduits()

    if meshobj.mesh.is_solved:
        autoupdate = AutoUpdateFD(meshobj.mesh, kmax=session.settings.solver.kmax)
        autoupdate()

        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_forces_conduit(tmax=session.settings.display.tmax)
        meshobj.display_reactions_conduit()

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit()

    meshobj.display_mesh_conduit()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Delete Edges")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
