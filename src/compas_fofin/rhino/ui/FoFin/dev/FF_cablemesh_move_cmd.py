from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_move"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]

    if cablemesh.move():
        ui.scene.update()
        ui.record()

    # provide the option to move in
    # - global coordinate space
    # - object coordinate space
    # - ...


if __name__ == "__main__":
    RunCommand(True)
