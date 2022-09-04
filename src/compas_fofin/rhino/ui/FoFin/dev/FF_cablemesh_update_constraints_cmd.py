from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System

import compas_rhino

from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_update_constraints"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    for vertex in mesh.vertices_where(is_anchor=True):
        constraint = mesh.vertex_attribute(vertex, "constraint")

        if not constraint or not constraint._rhino_guid:
            continue

        result, guid = System.Guid.TryParse(constraint._rhino_guid)

        if not result:
            continue

        obj = compas_rhino.find_object(guid)
        if not obj:
            continue

        cablemesh.update_constraint(vertex, obj)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
