#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD


def RunCommand():
    session = FoFinSession()

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    meshobj: RhinoCableMeshObject = session.scene.get_node_by_name(name="CableMesh")
    if not meshobj:
        return

    # =============================================================================
    # Clear conduits
    # =============================================================================

    meshobj.clear_conduits()

    meshobj.display_edges_conduit(thickness=session.settings.drawing.edge_thickness)
    meshobj.display_mesh_conduit()

    # =============================================================================
    # Update Constraints
    # =============================================================================

    for sceneobject in session.scene.objects:
        if isinstance(sceneobject, RhinoConstraintObject):
            sceneobject.update_constraint_geometry()

    meshobj.mesh.update_constraints()

    # =============================================================================
    # Update scene
    # =============================================================================

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
        meshobj.display_reactions_conduit(scale=session.settings.drawing.scale_reactions)

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit(thickness=session.settings.drawing.edge_thickness)

    meshobj.display_mesh_conduit()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Update Anchors")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
