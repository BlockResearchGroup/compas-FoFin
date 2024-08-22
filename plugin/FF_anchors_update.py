#! python3
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.scene import Scene
from compas_fd.constraints import Constraint
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.rhino.scene import RhinoConstraintObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    if not meshobj:
        return

    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Update Constraints
    # =============================================================================

    constraint: Constraint

    for sceneobject in scene.objects:
        if isinstance(sceneobject, RhinoConstraintObject):
            robj = compas_rhino.objects.find_object(sceneobject.guids[0])
            curve = compas_rhino.conversions.curveobject_to_compas(robj)
            sceneobject.constraint.geometry = curve

    for vertex in mesh.vertices():
        guid = mesh.vertex_attribute(vertex, "constraint")
        if guid:
            constraint = mesh.constraints[guid]
            constraint.location = mesh.vertex_point(vertex)
            constraint.project()
            mesh.vertex_attributes(vertex, "xyz", constraint.location)

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave"]:
        session.record(eventname="Update Anchors")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
