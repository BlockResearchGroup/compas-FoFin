#! python3
# venv: brg-csd
# r: compas_fofin>=0.15.2

import compas_rhino.objects
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_fofin.session import FoFinSession


def RunCommand():
    session = FoFinSession()

    session.clear_conduits()

    session.scene.redraw()

    meshobj: RhinoCableMeshObject = session.find_cablemesh()
    if not meshobj:
        return

    # =============================================================================
    # Remap constraints
    # =============================================================================

    for obj in session.scene.objects:
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
        meshobj.display_reactions_conduit(scale=session.settings.drawing.scale_reactions)

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit(thickness=session.settings.drawing.edge_thickness)

    meshobj.display_mesh_conduit()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
