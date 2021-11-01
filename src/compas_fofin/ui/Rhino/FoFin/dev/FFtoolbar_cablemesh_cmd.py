from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFcablemesh_from_mesh_cmd


__commandname__ = "FFtoolbar_cablemesh"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options = ["FromMesh", "FromSurface"]
    option = compas_rhino.rs.GetString("Create CableMesh:", strings=options)

    if not option:
        return

    if option == "FromMesh":
        FFcablemesh_from_mesh_cmd.RunCommand(True)

    elif option == "FromSurface":
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
