#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.scene import RhinoCableMeshObject
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
        meshobj.show_vertices = list(meshobj.mesh.vertices())
        meshobj.redraw_vertices()

        selected = meshobj.select_vertices()

        if selected:
            meshobj.mesh.vertices_attribute("is_support", True, keys=selected)

    elif option == "Remove":
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.redraw_vertices()

        selected = meshobj.select_vertices()

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
        session.record(name="Add/Remove Anchors")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
