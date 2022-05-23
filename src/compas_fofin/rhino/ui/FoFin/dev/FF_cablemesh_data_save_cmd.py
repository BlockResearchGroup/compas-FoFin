from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_ui.ui import UI


__commandname__ = 'FF_cablemesh_data_save'


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    path = ui.pick_file_save('FoFin.data')
    if path:
        compas.json_dump(mesh, path)


if __name__ == '__main__':
    RunCommand(True)
