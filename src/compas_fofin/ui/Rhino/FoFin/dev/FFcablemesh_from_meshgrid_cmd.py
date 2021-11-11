from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_from_meshgrid"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    dx = compas_rhino.rs.GetReal("Dimension in X direction:", 10.0, 1.0, 100.0)
    nx = compas_rhino.rs.GetInteger("Number of faces in X direction:", 10, 2, 100)
    dy = compas_rhino.rs.GetReal("Dimension in the Y direction:", dx, 1.0, 100.0)
    ny = compas_rhino.rs.GetInteger("Number of faces in Y direction:", nx, 2, 100)

    cablemesh = CableMesh.from_meshgrid(dx, nx, dy, ny)

    scene.clear()
    scene.add(cablemesh, name='cablemesh')
    scene.update()

    print("CableMesh object successfully created. Input mesh has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
