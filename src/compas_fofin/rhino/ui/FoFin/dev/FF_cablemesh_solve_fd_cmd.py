from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI


__commandname__ = 'FF_cablemesh_solve_fd'


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    fd = ui.proxy.function('compas_fd.fd.mesh_fd_constrained_numpy')

    result = fd(mesh)

    if not result:
        # this failure should just rigger an error
        print("Force-density method equilibrium failed!")
        return

    mesh.data = result.data
    cablemesh.is_valid = True

    ui.scene.update()
    # ui.record()


if __name__ == '__main__':
    RunCommand(True)
