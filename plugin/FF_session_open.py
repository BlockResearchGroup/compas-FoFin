#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_rhino.objects
from compas.colors import Color
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD
from compas_rui.forms import FileForm


def RunCommand(is_interactive):
    session = FoFinSession()

    filepath = FileForm.open(session.basedir)
    if not filepath:
        return

    session.clear()
    session.load(filepath)

    scene = session.scene()
    scene.draw()

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")
    if meshobj:
        # =============================================================================
        # Remap constraints
        # =============================================================================

        for sceneobject in scene.objects:
            if isinstance(sceneobject, RhinoConstraintObject):
                scene.clear_context(sceneobject.guids)
                scene.remove(sceneobject)

        for guid in meshobj.mesh.constraints:
            constraint = meshobj.mesh.constraints[guid]
            sceneobject = scene.add(constraint, color=Color.cyan())
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
            meshobj.display_reactions_conduit()

        else:
            meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
            meshobj.show_edges = False
            meshobj.show_faces = False
            meshobj.draw()
            meshobj.display_edges_conduit()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Open Session")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
