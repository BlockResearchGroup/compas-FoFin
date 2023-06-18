from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

import compas_rhino

# from compas_rhino.geometry import RhinoSurface

from compas_ui.ui import UI
from compas_fofin.rhino.conversions import curveobject_to_compas

from compas_fofin.rhino.objects import RhinoCableMeshObject
from compas_fd.constraints import Constraint
from compas.artists import Artist


__commandname__ = "FF_cablemesh_constraints"


@UI.error()
def RunCommand(is_interactive):
    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, RhinoCableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    compas_rhino.rs.UnselectAllObjects()

    options = ["Constrain", "Unconstrain"]
    option = ui.get_string("Constrain/Unconstrain nodes", options=options)
    if not option:
        return

    mesh = cablemesh.mesh
    cablemesh.is_valid = False

    if option == "Unconstrain":
        # Select any of the currently constrained vertices
        # and unconstrain them
        # leaving them as simple anchors
        nodes = ui.controller.mesh_select_vertices(cablemesh)
        if nodes:
            for node in nodes:
                cablemesh.mesh.unset_vertex_attribute(node, "constraint")

    elif option == "Constrain":
        # Select any set of vertices
        # Make them anchors and constrain them
        # cablemesh.settings["show.vertices:free"] = True
        ui.scene.update()

        vertices = ui.controller.mesh_select_vertices(cablemesh)
        if not vertices:
            return

        guid = compas_rhino.select_curve(message="Select constraint (Curve)")
        if not guid:
            return

        obj = compas_rhino.find_object(guid)
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
                curve = curveobject_to_compas(obj)
                constraint = Constraint(curve)
                artist = Artist(constraint)
                guids = artist.draw()
                compas_rhino.rs.HideObject(guid)
                guid = guids[0]
                constraint._rhino_guid = str(guid)

        else:
            raise NotImplementedError

        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, "xyz")
            constraint.project()
            mesh.vertex_attribute(vertex, "is_anchor", True)
            mesh.vertex_attributes(vertex, "xyz", constraint.location)
            mesh.vertex_attribute(vertex, "constraint", constraint)

    compas_rhino.rs.UnselectAllObjects()
    # cablemesh.settings["show.vertices:free"] = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
