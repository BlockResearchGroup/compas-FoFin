from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import get_proxy
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


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

    mesh_fd = proxy.function('compas_fd.fd.mesh_fd_numpy')

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    result = mesh_fd(cablemesh.datastructure)

    if not result:
        print("Force-density method equilibrium failed!")
        return

    cablemesh.datastructure = result

    scene.update()

    print('Equilibrium found!')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
