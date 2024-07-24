import pathlib

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
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

    option = rs.GetString(message="Constrain/Unconstrain nodes", strings=["Constrain", "Unconstrain"])
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
        meshobj.delete_vertices()
        meshobj.draw_vertices()

        vertices = meshobj.select_vertices()
        if not vertices:
            return

        guid = rs.GetObject(message="Select constraint (Curve)", preselect=True, select=True, filter=rs.filter.curve)
        if not guid:
            return

        obj = compas_rhino.objects.find_object(guid)
        if not obj:
            return

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:

            constraint = None
            for vertex in mesh.vertices():
                temp = mesh.vertex_attribute(vertex, "constraint")
                if temp is not None:
                    if temp._rhino_guid == str(guid):
                        constraint = temp
                        break

            if not constraint:
                curve = compas_rhino.conversions.curveobject_to_compas(obj)
                constraint = Constraint(curve)

                constraintobj = scene.add(constraint)
                scene.draw()

                rs.HideObject(constraintobj.guid)
                constraint._rhino_guid = str(guid)

        else:
            raise NotImplementedError

        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, "xyz")
            constraint.project()
            mesh.vertex_attribute(vertex, "is_anchor", True)
            mesh.vertex_attributes(vertex, "xyz", constraint.location)
            mesh.vertex_attribute(vertex, "constraint", constraint)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()
    meshobj.show_free = False

    guids = compas_rhino.objects.get_objects(name="CableMesh*")
    compas_rhino.objects.delete_objects(guids)

    scene.draw()

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
