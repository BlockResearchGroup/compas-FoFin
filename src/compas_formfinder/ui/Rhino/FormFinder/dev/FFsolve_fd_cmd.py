from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_formfinder.rhino import get_scene
from compas_formfinder.rhino import get_proxy
from compas_formfinder.rhino import FF_undo
from compas_formfinder.rhino import FF_error


__commandname__ = "FFsolve_fd"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    fd_xyz = proxy.function('compas_fofin.fofin.fd_xyz_numpy')

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    result = fd_xyz(cablemesh.datastructure.data)

    if not result:
        print("Force-density method equilibrium failed!")
        return

    cablemesh.datastructure.data = result

    cablemesh.settings['_is.valid'] = True

    scene.update()

    print('Equilibrium found!')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
