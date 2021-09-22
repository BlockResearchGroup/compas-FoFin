from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFcablemesh_modify_faces_cmd


__commandname__ = "FFtoolbar_cablemesh_modify_faces"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["FacesAttributes"]
    option = compas_rhino.rs.GetString("Modify CableMesh faces:", strings=options)

    if not option:
        return

    if option == "FacesAttributes":
        FFcablemesh_modify_faces_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
