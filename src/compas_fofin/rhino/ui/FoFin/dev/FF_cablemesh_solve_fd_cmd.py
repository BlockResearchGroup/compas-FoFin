from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System
import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_solve_fd"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    for vertex in cablemesh.mesh.vertices_where(is_anchor=True):
        constraint = cablemesh.mesh.vertex_attribute(vertex, "constraint")

        if not constraint or not constraint._rhino_guid:
            continue

        result, guid = System.Guid.TryParse(constraint._rhino_guid)
        if not result:
            continue

        obj = compas_rhino.find_object(guid)
        if not obj:
            continue

        cablemesh.update_constraint(vertex, obj)

    fd = ui.proxy.function("compas_fd.fd.mesh_fd_constrained_numpy")
    result = fd(cablemesh.mesh)

    if not result:
        # this failure should just rigger an error
        print("Force-density method equilibrium failed!")
        return

    cablemesh.mesh.data = result.data
    cablemesh.is_valid = True

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
