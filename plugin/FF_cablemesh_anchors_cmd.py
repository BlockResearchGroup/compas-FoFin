#! python3
import pathlib

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_session.session import Session

__commandname__ = "FF_cablemesh_anchors"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FoFin")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)
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

    option = rs.GetString(message="Select/Unselect anchors", strings=["Select", "Unselect"])
    if not option:
        return

    option_is_select = option == "Select"

    meshobj.is_valid = False  # this should be moved to the data
    meshobj.show_free = option_is_select

    while True:
        rs.UnselectAllObjects()

        vertices = meshobj.select_vertices(redraw=True)
        if not vertices:
            break

        mesh.vertices_attribute("is_anchor", option_is_select, keys=vertices)

        if not option_is_select:
            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_free = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    # session.record()
    # session.save_all()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
