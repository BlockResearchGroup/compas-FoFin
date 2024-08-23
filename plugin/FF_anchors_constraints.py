#! python3
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas_fd.constraints import Constraint
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
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
    # Modify Anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Constraints", strings=["Add", "Remove"])
    if not option:
        return

    if option == "Remove":

        vertices = meshobj.select_vertices(show_anchors=True, show_free=False)
        if not vertices:
            return

        for vertex in vertices:
            mesh.unset_vertex_attribute(vertex, "constraint")

    elif option == "Add":

        vertices = meshobj.select_vertices(show_anchors=True, show_free=True)
        if not vertices:
            return

        # Select the Constraint
        # -----------------------------------

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

        # -----------------------------------

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

    meshobj.show_anchors = True
    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.CONFIG["autosave.events"]:
        session.record(eventname=f"{option} Constraints")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
