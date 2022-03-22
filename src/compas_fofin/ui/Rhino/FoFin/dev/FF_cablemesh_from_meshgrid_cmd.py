from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.app import App

from compas_fofin.datastructures import CableMesh


__commandname__ = 'FF_cablemesh_from_meshgrid'


@App.error()
def RunCommand(is_interactive):

    app = App()

    dx = app.get_real("Dimension in the X direction?", minval=1, maxval=100, default=10)
    if not dx:
        return

    dy = app.get_real("Dimension in the Y direction?", minval=1, maxval=100, default=dx)
    if not dy:
        return

    nx = app.get_integer("Number of faces in the X direction?", minval=1, maxval=1000, default=10)
    if not nx:
        return

    ny = app.get_integer("Number of faces in the Y direction?", minval=1, maxval=1000, default=nx)
    if not ny:
        return

    mesh = CableMesh.from_meshgrid(dx=dx, nx=nx, dy=dy, ny=ny)
    mesh.name = 'CableMesh'

    app.scene.clear()
    app.scene.add(mesh, name=mesh.name)
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
