from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

import compas_rhino
from compas_rhino.geometry import RhinoSurface

from compas_ui.ui import UI
from compas_fofin.rhino.conversions import curveobject_to_compas

from compas_fofin.rhino.objects import RhinoCableMeshObject
from compas_fd.constraints import Constraint


__commandname__ = "FF_cablemesh_constrain_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, RhinoCableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    vertices = ui.controller.mesh_select_vertices(cablemesh)
    if not vertices:
        return

    guid = compas_rhino.select_curve(message="Select constraint (Curve/Surface)")
    if not guid:
        return

    obj = compas_rhino.find_object(guid)
    if not obj:
        return

    if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:

        curve = curveobject_to_compas(obj)
        constraint = Constraint(curve)

    elif obj.ObjectType == Rhino.DocObjects.ObjectType.Surface:

        guid = compas_rhino.select_surface(message="Select surface constraint")
        if not guid:
            return

        surface = RhinoSurface.from_guid(guid).to_compas()
        constraint = Constraint(surface)

    else:
        raise NotImplementedError

    constraint._rhino_guid = str(guid)

    for vertex in vertices:
        constraint.location = mesh.vertex_attributes(vertex, "xyz")
        constraint.project()
        mesh.vertex_attributes(vertex, "xyz", constraint.location)
        mesh.vertex_attribute(vertex, "constraint", constraint)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
