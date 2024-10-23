#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import compas_rhino.objects
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession


def RunCommand(is_interactive):
    session = FoFinSession()

    session.clear_conduits()

    scene = session.scene()

    scene.redraw()

    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")
    if not meshobj:
        return

    # =============================================================================
    # Remap constraints
    # =============================================================================

    for obj in scene.objects:
        if isinstance(obj, RhinoConstraintObject):
            robj = compas_rhino.objects.find_object(obj.guids[0])
            robj.UserDictionary["constraint.guid"] = str(obj.constraint.guid)

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj.clear()

    if meshobj.mesh.is_solved:
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
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
