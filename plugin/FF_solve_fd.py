#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_fofin.settings
from compas.geometry import Vector
from compas_fd.loads import SelfweightCalculator
from compas_fd.solvers import fd_constrained_numpy
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
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
    # Update Constraints
    # =============================================================================

    if compas_fofin.settings.SETTINGS["FormFinder"]["autoupdate.constraints"]:

        for sceneobject in scene.objects:
            if isinstance(sceneobject, RhinoConstraintObject):
                sceneobject.update_constraint_geometry()

        mesh.update_constraints()

    # =============================================================================
    # Solve FD
    # =============================================================================

    kmax = compas_fofin.settings.SETTINGS["Solvers"]["constraints.maxiter"] or 100

    vertex_index = mesh.vertex_index()

    vertices = mesh.vertices_attributes("xyz")

    loads = [mesh.vertex_attributes(vertex, ["px", "py", "pz"]) or [0, 0, 0] for vertex in mesh.vertices()]
    fixed = [vertex_index[vertex] for vertex in mesh.vertices_where(is_support=True)]
    edges = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

    selfweight = SelfweightCalculator(mesh, mesh.attributes["density"], thickness_attr_name="thickness")

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
        selfweight=selfweight,
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

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(name="Solve FD")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
