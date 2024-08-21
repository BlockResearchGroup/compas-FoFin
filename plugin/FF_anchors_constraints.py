#! python3
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.scene import Scene
from compas_fd.constraints import Constraint
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

    # constraints = session.setdefault("constraints", factory=dict)

    # =============================================================================
    # Modify Anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Constraints", strings=["Add", "Remove"])
    if not option:
        return

    # this should be moved to the data
    meshobj.is_valid = False

    if option == "Remove":
        # Select any of the currently constrained vertices
        # and unconstrain them leaving them as simple anchors

        vertices = meshobj.select_vertices()
        if vertices:
            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

    elif option == "Add":
        # Select any set of vertices
        # Make them anchors and constrain them

        vertices = meshobj.select_vertices(redraw=True)
        if not vertices:
            return

        guid = rs.GetObject(message="Select constraint (Curve)", preselect=True, select=True, filter=rs.filter.curve)
        if not guid:
            return

        robj = compas_rhino.objects.find_object(guid)
        if not robj:
            return

        constraint = None
        if "constraint.guid" in robj.UserDictionary:
            if robj.UserDictionary["constraint.guid"] in mesh.constraints:
                # the constraint already exists
                constraint = mesh.constraints[robj.UserDictionary["constraint.guid"]]

        if not constraint:
            curve = compas_rhino.conversions.curveobject_to_compas(robj)
            constraint = Constraint(curve)
            sceneobject = scene.add(constraint, color=Color.cyan())
            sceneobject.draw()

            robj = compas_rhino.objects.find_object(sceneobject.guids[0])
            robj.UserDictionary["constraint.guid"] = str(constraint.guid)

            mesh.constraints[str(constraint.guid)] = constraint
            rs.HideObject(guid)

        if constraint:
            for vertex in vertices:
                constraint.location = mesh.vertex_point(vertex)
                constraint.project()

                mesh.vertex_attribute(vertex, "is_anchor", True)
                mesh.vertex_attribute(vertex, "constraint", str(constraint.guid))
                mesh.vertex_attributes(vertex, "xyz", constraint.location)

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

    if session.CONFIG["autosave"]:
        session.record(eventname=f"{option} Constraints")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
