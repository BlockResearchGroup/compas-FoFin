#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD
from compas_fofin.solvers import InteractiveScaleFD

# =============================================================================
# Command
# =============================================================================


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

    option = rs.GetString(message="Update ForceDensity", strings=["Value", "ScaleFactor", "Interactive"])
    if not option:
        return

    selectable = list(meshobj.mesh.edges())
    selected = meshobj.select_edges(selectable)

    if selected:
        if option == "Value":
            value = rs.GetReal(message="Value")
            meshobj.mesh.edges_attribute("q", value, keys=selected)

        elif option == "ScaleFactor":
            factor = rs.GetReal(message="ScaleFactor")
            for edge in selected:
                q = meshobj.mesh.edge_attribute(edge, "q")
                meshobj.mesh.edge_attribute(edge, "q", q * factor)

        elif option == "Interactive":
            interactive = InteractiveScaleFD(meshobj.mesh, selected)
            interactive()

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
