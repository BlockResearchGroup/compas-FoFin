#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import rhinoscriptsyntax as rs  # type: ignore

import compas_fofin.settings
import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas_fd.constraints import Constraint
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")

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

        meshobj.show_vertices = True
        meshobj.show_free = False
        meshobj.show_supports = True

        rs.EnableRedraw(False)
        meshobj.clear_vertices()
        meshobj.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = meshobj.select_vertices()

        if vertices:
            meshobj.show_vertices = vertices

            rs.EnableRedraw(False)
            meshobj.clear_vertices()
            meshobj.draw_vertices()
            rs.EnableRedraw(True)
            rs.Redraw()

            for vertex in vertices:
                mesh.unset_vertex_attribute(vertex, "constraint")

    elif option == "Add":

        meshobj.show_vertices = True
        meshobj.show_free = True
        meshobj.show_supports = True

        rs.EnableRedraw(False)
        meshobj.clear_vertices()
        meshobj.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = meshobj.select_vertices()

        if vertices:

            meshobj.show_vertices = vertices

            rs.EnableRedraw(False)
            meshobj.clear_vertices()
            meshobj.draw_vertices()
            rs.EnableRedraw(True)
            rs.Redraw()

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

                    mesh.vertex_attribute(vertex, "is_support", True)
                    mesh.vertex_attribute(vertex, "constraint", str(constraint.guid))
                    mesh.vertex_attributes(vertex, "xyz", constraint.location)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.show_vertices = True
    meshobj.show_supports = True
    meshobj.show_free = False
    meshobj.show_edges = False

    meshobj.clear()
    meshobj.draw()

    # =============================================================================
    # Session save
    # =============================================================================

    if compas_fofin.settings.SETTINGS["FormFinder"]["autosave.events"]:
        session.record(name=f"{option} Constraints")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
