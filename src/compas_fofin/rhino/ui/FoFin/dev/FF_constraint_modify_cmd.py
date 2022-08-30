from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import compas_rhino
from compas_ui.ui import UI


__commandname__ = "FF_constraint_modify"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    # result = ui.scene.get(name="CableMesh")
    # if not result:
    #     raise Exception("There is no cablemesh in the scene.")

    # cablemesh = result[0]

    # nodes = ui.controller.mesh_select_vertices(cablemesh)
    # if not nodes:
    #     return

    # options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    # direction = ui.get_string(message="Direction.", options=options)
    # if not direction:
    #     return

    # if direction == "Free":
    #     result = cablemesh.move_vertices(nodes)
    # else:
    #     result = cablemesh.move_vertices_direction(nodes, direction=direction)

    # if result:
    #     cablemesh.is_valid = False
    #     ui.scene.update()
    #     ui.record()

    # compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
