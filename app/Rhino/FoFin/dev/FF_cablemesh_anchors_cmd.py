from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.rhino.forms import error
from compas_ui.app import App


__commandname__ = 'FF_cablemesh_anchors'


@error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    options = ['Select', 'Unselect']
    modes = ['AllBoundaryNodes', 'Corners', 'ByContinuousEdges', 'Manual']

    option = app.get_string('Select/Unselect anchors.', options=options)
    if not option:
        return

    is_anchor = option == 'Select'

    while True:
        compas_rhino.rs.UnselectAllObjects()
        cablemesh.settings['show.vertices:free'] = True
        app.scene.update()

        mode = app.get_string('Selection mode?', options=modes)
        if not mode:
            break

        if mode == 'AllBoundaryNodes':
            vertices = list(set(flatten(mesh.vertices_on_boundaries())))

        elif mode == 'Corners':
            vertices = mesh.corner_vertices()

        elif mode == 'ByContinuousEdges':
            edges = cablemesh.select_edges()
            vertices = list(set(flatten([mesh.vertices_on_edge_loop(edge) for edge in edges])))

        elif mode == 'Manual':
            vertices = cablemesh.select_vertices()

        if vertices:
            cablemesh.settings['_is.valid'] = False
            mesh.vertices_attribute('is_anchor', is_anchor, keys=vertices)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.settings['show.vertices:free'] = False
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
