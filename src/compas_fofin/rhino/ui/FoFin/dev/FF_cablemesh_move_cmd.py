from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_move"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    if cablemesh.move():
        ui.scene.update()
        ui.record()

    # provide the option to move in
    # - global coordinate space
    # - object coordinate space
    # - ...


if __name__ == "__main__":
    RunCommand(True)
