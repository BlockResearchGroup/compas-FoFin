#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import rhinoscriptsyntax as rs  # type: ignore

import compas_fofin.settings
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Preselect anchors
    # =============================================================================

    fixed = list(mesh.vertices_where(is_fixed=True))
    leaves = list(mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        mesh.vertices_attribute("is_support", True, keys=vertices)

    # =============================================================================
    # Select/Unselect anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Anchors", strings=["Add", "Remove"])
    if not option:
        return

    if option == "Add":

        meshobj.show_vertices = True
        meshobj.show_free = True
        meshobj.show_supports = True

        rs.EnableRedraw(False)
        meshobj.clear_vertices()
        meshobj.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = meshobj.select_vertices()

        if vertices:
            mesh.vertices_attribute("is_support", True, keys=vertices)

    elif option == "Remove":

        meshobj.show_vertices = True
        meshobj.show_free = False
        meshobj.show_supports = True

        rs.EnableRedraw(False)
        meshobj.clear_vertices()
        meshobj.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = meshobj.select_vertices()

        if vertices:
            mesh.vertices_attribute("is_support", False, keys=vertices)
            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_vertices = True
    meshobj.show_supports = True
    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(name="Add/Remove Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
