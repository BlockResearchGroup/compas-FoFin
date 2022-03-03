from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.app import App
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFsolve_fd"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    app = App()

    mesh_fd = app.proxy.function('compas_fd.fd.mesh_fd_constrained_numpy')

    cablemesh = app.scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    result = mesh_fd(cablemesh.datastructure)

    if not result:
        print("Force-density method equilibrium failed!")
        return

    cablemesh.datastructure.data = result.data

    cablemesh.settings['_is.valid'] = True

    app.scene.update()

    print('Equilibrium found!')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
