#! python3
from compas.geometry import Vector
from compas_fd.solvers import fd_constrained_numpy
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.rhino.scene import RhinoConstraintObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Update Constraints
    # =============================================================================

    if session.CONFIG["autoupdate.constraints"]:

        for sceneobject in scene.objects:
            if isinstance(sceneobject, RhinoConstraintObject):
                sceneobject.update_constraint_geometry()

        mesh.update_constraints()

    # =============================================================================
    # Solve FD
    # =============================================================================

    kmax = session.CONFIG["solvers.fd.kmax"] or 100

    vertices = mesh.vertices_attributes("xyz")
    loads = [mesh.vertex_attribute(vertex, "load") or [0, 0, 0] for vertex in mesh.vertices()]
    fixed = list(mesh.vertices_where(is_anchor=True))
    edges = list(mesh.edges())
    q = list(mesh.edges_attribute("q"))

    constraints = [None] * len(vertices)
    for index, vertex in enumerate(mesh.vertices()):
        guid = mesh.vertex_attribute(vertex, "constraint")
        if guid:
            constraint = mesh.constraints[guid]
            constraints[index] = constraint

    result = fd_constrained_numpy(
        vertices=vertices,
        fixed=fixed,
        edges=edges,
        forcedensities=q,
        loads=loads,
        constraints=constraints,
        kmax=kmax,
    )

    for index, (vertex, attr) in enumerate(mesh.vertices(data=True)):
        attr["x"] = result.vertices[index, 0]
        attr["y"] = result.vertices[index, 1]
        attr["z"] = result.vertices[index, 2]
        attr["_residual"] = Vector(*result.residuals[index])

    for index, (edge, attr) in enumerate(mesh.edges(data=True)):
        attr["_f"] = result.forces[index]

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Solve FD")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
