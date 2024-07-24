import pathlib
import random

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino.objects
from compas.scene import Scene
from compas_fd.solvers import fd_numpy
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_session.session import Session

__commandname__ = "FF_cablemesh_solve_fd"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FoFin")

    print(session.data)
    print(session.datamap)

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")
    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Solve FD
    # =============================================================================

    # for edge in mesh.edge_sample(size=5):
    #     mesh.edge_attribute(edge, 'q', random.randint(1, 50))

    mesh.edges_attribute('q', 1.0)

    vertices = mesh.vertices_attributes("xyz")
    fixed = list(mesh.vertices_where(is_anchor=True))
    edges = list(mesh.edges())
    loads = [[0, 0, 0] for _ in range(len(vertices))]
    q = list(mesh.edges_attribute('q'))

    result = fd_numpy(
        vertices=vertices,
        fixed=fixed,
        edges=edges,
        forcedensities=q,
        loads=loads,
    )

    for vertex, attr in mesh.vertices(data=True):
        attr["x"] = result.vertices[vertex, 0]
        attr["y"] = result.vertices[vertex, 1]
        attr["z"] = result.vertices[vertex, 2]

    meshobj.vertex_xyz = None

    # =============================================================================
    # Update scene
    # =============================================================================

    guids = compas_rhino.objects.get_objects(name="CableMesh*")
    compas_rhino.objects.delete_objects(guids)

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
