#! python3
import pathlib

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.scene import Scene
from compas_fd.constraints import Constraint
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_session.session import Session

__commandname__ = "FF_cablemesh_constraints"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FoFin")

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.get("scene")

    meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")  # replace by: get_object_by_name (cf. jQuery)
    mesh: CableMesh = meshobj.mesh

    # =============================================================================
    # Update constraints
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Constrain/Unconstrain Vertices", strings=["Constrain", "Unconstrain"])
    if not option:
        return

    # this should be moved to the data
    meshobj.is_valid = False

    if option == "Unconstrain":
        # Select any of the currently constrained vertices
        # and unconstrain them leaving them as simple anchors

        vertices = meshobj.select_vertices()
        if vertices:
            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

    elif option == "Constrain":
        # Select any set of vertices
        # Make them anchors and constrain them

        meshobj.show_free = True

        vertices = meshobj.select_vertices(redraw=True)
        if vertices:

            guid = rs.GetObject(message="Select constraint (Curve)", preselect=True, select=True, filter=rs.filter.curve)
            if guid:

                obj = compas_rhino.objects.find_object(guid)
                if obj:

                    constraint = None
                    if "constraint.guid" in obj.UserDictionary:
                        if obj.UserDictionary["constraint.guid"] in mesh.constraints:
                            constraint = mesh.constraints[obj.UserDictionary["constraint.guid"]]

                    if not constraint:
                        curve = compas_rhino.conversions.curveobject_to_compas(obj)
                        constraint = Constraint(curve)
                        obj = scene.add(constraint.geometry, color=Color.cyan())  # only the gometry of the constraint is visualised
                        obj.draw()

                        obj = compas_rhino.objects.find_object(obj.guids[0])
                        obj.UserDictionary["constraint.guid"] = str(constraint.guid)
                        mesh.constraints[str(constraint.guid)] = constraint
                        rs.HideObject(guid)

                    if constraint:
                        for vertex in vertices:
                            constraint.location = mesh.vertex_point(vertex)
                            constraint.project()

                            mesh.vertex_attribute(vertex, "is_anchor", True)
                            mesh.vertex_attribute(vertex, "constraint", constraint)
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

    # session.record()
    # session.save_all()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
