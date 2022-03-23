from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_ui.app import App


__commandname__ = 'FF_cablemesh_data_save'


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    path = app.pick_file_save('FoFin.data')
    if path:
        compas.json_dump(mesh, path)


if __name__ == '__main__':
    RunCommand(True)
