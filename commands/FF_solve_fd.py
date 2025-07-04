#! python3
# venv: brg-csd
# r: compas_fofin>=0.15.3

from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD


def RunCommand():
    session = FoFinSession()

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    meshobj: RhinoCableMeshObject = session.find_cablemesh()
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

    for sceneobject in session.scene.objects:
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
    meshobj.display_reactions_conduit(scale=session.settings.drawing.scale_reactions)
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
    RunCommand()
