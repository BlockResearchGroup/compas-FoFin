#! python3
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas.scene import Scene
from compas_fd.solvers import fd_constrained_numpy
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session

__commandname__ = "FF_solve_fd"


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Solve FD
    # =============================================================================

    vertices = mesh.vertices_attributes("xyz")
    fixed = list(mesh.vertices_where(is_anchor=True))
    edges = list(mesh.edges())
    loads = [[0, 0, 0] for _ in range(len(vertices))]
    q = list(mesh.edges_attribute("q"))

    constraints = [None] * len(vertices)
    for index, vertex in enumerate(mesh.vertices()):
        constraint = mesh.vertex_attribute(vertex, "constraint")
        constraints[index] = constraint

    result = fd_constrained_numpy(
        vertices=vertices,
        fixed=fixed,
        edges=edges,
        forcedensities=q,
        loads=loads,
        constraints=constraints,
    )

    for vertex, attr in mesh.vertices(data=True):
        attr["x"] = result.vertices[vertex, 0]
        attr["y"] = result.vertices[vertex, 1]
        attr["z"] = result.vertices[vertex, 2]

    # =============================================================================
    # Update scene
    # =============================================================================

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
