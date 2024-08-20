#! python3
import pathlib

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_session.session import Session

__commandname__ = "FF_cablemesh_edges_delete"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FoFin")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Delete edges
    # =============================================================================

    edges = meshobj.select_edges()

    if edges:
        fkeys = set()
        for edge in edges:
            fkeys.update(mesh.edge_faces(edge))

        for fkey in fkeys:
            if fkey is not None:
                mesh.delete_face(fkey)

        mesh.remove_unused_vertices()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    scene.clear()
    scene.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    # session.record()
    # session.save()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
