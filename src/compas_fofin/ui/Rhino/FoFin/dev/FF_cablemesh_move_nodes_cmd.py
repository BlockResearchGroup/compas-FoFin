from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.app import App


__commandname__ = "FF_cablemesh_move_nodes"


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]

    nodes = app.select_mesh_vertices(cablemesh)
    if not nodes:
        return

    options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    direction = app.get_string(message="Direction.", options=options)
    if not direction:
        return

    if direction == 'Free':
        result = cablemesh.move_vertices(nodes)
    else:
        result = cablemesh.move_vertices_direction(nodes, direction=direction)

    if result:
        cablemesh.is_valid = False
        app.scene.update()
        app.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
