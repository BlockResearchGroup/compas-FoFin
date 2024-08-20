#! python3
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session

__commandname__ = "FF_anchors"


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: find (cf. jQuery)
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Preselect anchors
    # =============================================================================

    fixed = list(mesh.vertices_where(is_fixed=True))
    leaves = list(mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        mesh.vertices_attribute("is_anchor", True, keys=vertices)

    # =============================================================================
    # Select/Unselect anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Anchors", strings=["Select", "Unselect"])
    if not option:
        return

    if option == "Select":

        mechanism = rs.GetString(message="Select", strings=["Degree", "Loop", "Manual"])
        if not mechanism:
            return

        if mechanism == "Degree":
            D = rs.GetInteger(message="Vertex Degree", number=2, minimum=1)
            if not D:
                return

            vertices = mesh.vertices_where(vertex_degree=D)
            if not vertices:
                return

            mesh.vertices_attribute("is_anchor", True, keys=vertices)

        elif mechanism == "Loop":

            meshobj.show_edges = True
            edges = meshobj.select_edges(redraw=True)
            if not edges:
                return

            vertices = []
            for edge in edges:
                for u, v in mesh.edge_loop(edge):
                    vertices.append(u)
                    vertices.append(v)
            vertices = list(set(vertices))
            if not vertices:
                return

            mesh.vertices_attribute("is_anchor", True, keys=vertices)

        elif mechanism == "Manual":

            meshobj.show_free = True
            vertices = meshobj.select_vertices(redraw=True)
            if not vertices:
                return

            mesh.vertices_attribute("is_anchor", True, keys=vertices)

    elif option == "Unselect":

        meshobj.show_free = False
        vertices = meshobj.select_vertices(redraw=True)
        if not vertices:
            return

        mesh.vertices_attribute("is_anchor", False, keys=vertices)
        for vertex in vertices:
            mesh.unset_vertex_attribute(vertex, "constraint")

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.is_valid = False

    meshobj.show_free = False
    meshobj.show_edges = False

    # meshobj.clear_vertices()
    # meshobj.clear_edges()
    # meshobj.draw_vertices()
    # meshobj.draw_edges()
    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave"]:
        session.record()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
