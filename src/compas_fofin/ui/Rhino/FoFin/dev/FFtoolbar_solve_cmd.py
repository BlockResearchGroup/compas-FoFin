from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFtoolbar_solve"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["ForceDensity", "NaturalForceDensity", "DynamicRelaxation"]
    option = compas_rhino.rs.GetString("Solver:", strings=options)

    if not option:
        return

    if option == "ForceDensity":
        FFsolve_fd_cmd.RunCommand(True)

    elif option == "NaturalForceDensity":
        raise NotImplementedError

    elif option == "DynamicRelaxation":
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
