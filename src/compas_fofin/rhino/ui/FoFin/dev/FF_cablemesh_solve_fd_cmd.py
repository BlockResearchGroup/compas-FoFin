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
    cablemesh.update_equilibrium(ui)

    cablemesh.settings["show.edges"] = cablemesh.is_valid != True

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
