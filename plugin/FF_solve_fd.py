#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
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

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Clear conduits
    # =============================================================================

    session.clear_conduits()

    # =============================================================================
    # Update Constraints
    # =============================================================================

    for sceneobject in scene.objects:
        if isinstance(sceneobject, RhinoConstraintObject):
            sceneobject.update_constraint_geometry()

    mesh.update_constraints()

    # =============================================================================
    # Solve FD
    # =============================================================================

    autoupdate = AutoUpdateFD(meshobj.mesh, kmax=session.settings.solver.kmax)
    autoupdate()

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
    meshobj.show_edges = False
    meshobj.show_faces = False

    meshobj.clear()
    meshobj.draw()
    meshobj.display_forces_conduit(tmax=session.settings.display.tmax)
    meshobj.display_reactions_conduit()
    meshobj.display_mesh_conduit()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Solve FD")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
