from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from compas_fofin.datastructures import CableMesh


__commandname__ = "FF_cablemesh_from_meshgrid"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    nx = ui.get_integer(
        "Number of faces in the X direction",
        minval=1,
        maxval=1000,
        default=10,
    )
    if not nx:
        return

    ny = ui.get_integer(
        "Number of faces in the Y direction",
        minval=1,
        maxval=1000,
        default=nx,
    )
    if not ny:
        return

    dx = ui.get_real(
        "Dimension in the X direction",
        minval=1,
        maxval=100,
        default=10,
    )
    if not dx:
        return

    dy = ui.get_real(
        "Dimension in the Y direction",
        minval=1,
        maxval=100,
        default=dx,
    )
    if not dy:
        return

    mesh = CableMesh.from_meshgrid(dx=dx, nx=nx, dy=dy, ny=ny)
    mesh.name = "CableMesh"

    ui.scene.add(mesh, name=mesh.name)
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
