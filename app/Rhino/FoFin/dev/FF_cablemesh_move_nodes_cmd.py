from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten

from compas_ui.rhino.forms import error
from compas_ui.app import App


__commandname__ = "FF_cablemesh_move_nodes"


@error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
    direction = app.get_string(message="Direction.", options=options)
    if not direction:
        return

    options = ["ByContinuousEdges", "Manual"]
    mode = app.get_string(message="Selection Type.", options=options)
    if not mode:
        return

    if mode == "ByContinuousEdges":
        edges = cablemesh.select_edges()
        vertices = list(set(flatten([mesh.vertices_on_edge_loop(edge) for edge in edges])))
        cablemesh.selected_vertices = vertices

    elif mode == "Manual":
        vertices = cablemesh.select_vertices()

    if vertices:
        if direction == 'Free':
            move = cablemesh.move_vertices(vertices)
        else:
            move = cablemesh.move_vertices_direction(vertices, direction=direction)

        if move:
            cablemesh.is_valid = False
            app.scene.update()
            app.record()

        compas_rhino.rs.UnselectAllObjects()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
