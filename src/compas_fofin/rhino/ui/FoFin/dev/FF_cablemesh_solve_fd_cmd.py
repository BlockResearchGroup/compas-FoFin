from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_solve_fd"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    cablemesh.update_constraints()

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
