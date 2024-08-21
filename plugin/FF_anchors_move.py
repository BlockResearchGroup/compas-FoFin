#! python3
import rhinoscriptsyntax as rs  # type: ignore

from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Move anchors
    # =============================================================================

    mdir_options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    mdir = rs.GetString(message="Set Direction.", strings=mdir_options)
    if not mdir:
        return

    stype_options = ["ByContinuousEdges", "Manual"]
    stype = rs.GetString(message="Selection Type.", strings=stype_options)
    if not stype:
        return

    if stype == "ByContinuousEdges":
        meshobj.show_edges = True
        edges = meshobj.select_edges()
        if not edges:
            return

        vertices = []
        for edge in edges:
            for u, v in mesh.edge_loop(edge):
                vertices.append(u)
                vertices.append(v)
        vertices = list(set(vertices))
        vertices = [vertex for vertex in vertices if mesh.vertex_attribute(vertex, "is_anchor")]
        if not vertices:
            return

    elif stype == "Manual":
        vertices = meshobj.select_vertices()
        if not vertices:
            return

    if mdir == "Free":
        meshobj.move_vertices(vertices)
    else:
        meshobj.move_vertices_direction(vertices, direction=mdir)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.is_valid = False

    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave"]:
        session.record(eventname="Move Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
