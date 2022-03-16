from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms.error import error
from compas_ui.app import App
from compas_fofin.datastructures import CableMesh


__commandname__ = 'FF_cablemesh_from_meshgrid'


@error()
def RunCommand(is_interactive):

    app = App()

    mesh = CableMesh.from_meshgrid(10, 10)
    mesh.name = 'CableMesh'

    app.scene.clear()
    app.scene.add(mesh)
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
