from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_move_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    nodes = ui.controller.mesh_select_vertices(cablemesh)
    if not nodes:
        return

    options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    direction = ui.get_string(message="Direction", options=options)
    if not direction:
        return

    if direction == "Free":
        result = cablemesh.move_vertices(nodes)
    else:
        result = cablemesh.move_vertices_direction(nodes, direction=direction)

    if result:
        cablemesh.is_valid = False

        ui.scene.update()
        ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
