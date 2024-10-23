#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas_fd.constraints import Constraint
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_fofin.solvers import AutoUpdateFD


def RunCommand(is_interactive):
    session = FoFinSession()

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")
    if not meshobj:
        return

    # =============================================================================
    # Clear conduits
    # =============================================================================

    meshobj.clear_conduits()

    meshobj.display_edges_conduit()
    meshobj.display_mesh_conduit()

    # =============================================================================
    # Modify Anchors
    # =============================================================================

    rs.UnselectAllObjects()

    option = rs.GetString(message="Constraints", strings=["Add", "Remove"])
    if not option:
        return

    if option == "Remove":
        selectable = list(meshobj.mesh.vertices_where(is_support=True))
        selected = meshobj.select_vertices(selectable)

        if selected:
            for vertex in selected:
                meshobj.mesh.unset_vertex_attribute(vertex, "constraint")

    elif option == "Add":
        selectable = list(meshobj.mesh.vertices())
        selected = meshobj.select_vertices(selectable)

        if selected:
            meshobj.show_vertices = selected
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
                if robj.UserDictionary["constraint.guid"] in meshobj.mesh.constraints:
                    # the constraint already exists
                    constraint = meshobj.mesh.constraints[robj.UserDictionary["constraint.guid"]]

            if not constraint:
                curve = compas_rhino.conversions.curveobject_to_compas(robj)
                constraint = Constraint(curve)
                sceneobject = scene.add(constraint, color=Color.cyan())
                sceneobject.draw()

                robj = compas_rhino.objects.find_object(sceneobject.guids[0])
                robj.UserDictionary["constraint.guid"] = str(constraint.guid)

                meshobj.mesh.constraints[str(constraint.guid)] = constraint
                rs.HideObject(guid)

            # -----------------------------------
            # -----------------------------------

            if constraint:
                for vertex in selected:
                    constraint.location = meshobj.mesh.vertex_point(vertex)
                    constraint.project()

                    meshobj.mesh.vertex_attribute(vertex, "is_support", True)
                    meshobj.mesh.vertex_attribute(vertex, "constraint", str(constraint.guid))
                    meshobj.mesh.vertex_attributes(vertex, "xyz", constraint.location)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    meshobj.clear()
    meshobj.clear_conduits()

    if meshobj.mesh.is_solved:
        autoupdate = AutoUpdateFD(meshobj.mesh, kmax=session.settings.solver.kmax)
        autoupdate()

        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_forces_conduit(tmax=session.settings.display.tmax)
        meshobj.display_reactions_conduit()

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit()

    meshobj.display_mesh_conduit()

    # =============================================================================
    # Session save
    # =============================================================================

    if session.settings.autosave:
        session.record(name=f"{option} Constraints")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
