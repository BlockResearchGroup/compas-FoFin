#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

import compas_rhino.objects
from compas.colors import Color
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD
from compas_rui.forms import FileForm


def RunCommand():
    session = FoFinSession()

    filepath = FileForm.open(session.basedir)
    if not filepath:
        return

    session.clear()
    session.load(filepath)

    session.scene.draw()

    meshobj: RhinoCableMeshObject = session.scene.get_node_by_name(name="CableMesh")
    if meshobj:
        # =============================================================================
        # Remap constraints
        # =============================================================================

        for sceneobject in session.scene.objects:
            if isinstance(sceneobject, RhinoConstraintObject):
                session.scene.clear_context(sceneobject.guids)
                session.scene.remove(sceneobject)

        for guid in meshobj.mesh.constraints:
            constraint = meshobj.mesh.constraints[guid]
            sceneobject = session.scene.add(constraint, color=Color.cyan())
            sceneobject.draw()

            robj = compas_rhino.objects.find_object(sceneobject.guids[0])
            robj.UserDictionary["constraint.guid"] = str(guid)

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

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Open Session")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
