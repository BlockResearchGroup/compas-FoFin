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
    # Preselect anchors
    # =============================================================================

    fixed = list(meshobj.mesh.vertices_where(is_fixed=True))
    leaves = list(meshobj.mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        meshobj.mesh.vertices_attribute("is_support", True, keys=vertices)

    # =============================================================================
    # Select/Unselect anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Anchors", strings=["Add", "Remove"])
    if not option:
        return

    if option == "Add":
        selectable = list(meshobj.mesh.vertices())
        selected = meshobj.select_vertices(selectable)

        if selected:
            meshobj.mesh.vertices_attribute("is_support", True, keys=selected)

    elif option == "Remove":
        selectable = list(meshobj.mesh.vertices_where(is_support=True))
        selected = meshobj.select_vertices(selectable)

        if selected:
            meshobj.mesh.vertices_attribute("is_support", False, keys=selected)
            for vertex in selected:
                meshobj.mesh.unset_vertex_attribute(vertex, "constraint")

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
        session.record(name="Add/Remove Anchors")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
