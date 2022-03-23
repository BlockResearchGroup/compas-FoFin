from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_ui.app import App
from compas_fofin.datastructures import CableMesh


__commandname__ = 'FF_cablemesh_data_load'


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]

    path = app.pick_file_open()
    if path:
        mesh = compas.json_load(path)
        name = cablemesh.name
        settings = cablemesh.settings.copy()
        app.scene.clear()
        app.scene.add(CableMesh.from_data(mesh.data), name=name, settings=settings)
        app.scene.update()
        app.record()


if __name__ == '__main__':
    RunCommand(True)
