from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_formfinder.rhino import get_scene
from compas_formfinder.rhino import FF_error

import FFcablemesh_from_mesh_cmd


__commandname__ = "FFtoolbar_cablemesh"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options1 = ["FromGeometry", "FromFile"]
    option1 = compas_rhino.rs.GetString("Create CableMesh:", strings=options1)

    if not option1:
        return

    if option1 == "FromGeometry":
        options2 = ["FromMesh", "FromSurface", "FromTriangulation", "FromSkeleton", "FromFeatures"]
        option2 = compas_rhino.rs.GetString("Selection mode:", strings=options2)

        if not option2:
            return

        if option2 == "FromMesh":
            FFcablemesh_from_mesh_cmd.RunCommand(True)

        elif option2 == "FromSurface":
            raise NotImplementedError

        elif option2 == "FromTriangulation":
            raise NotImplementedError

        elif option2 == "FromSkeleton":
            raise NotImplementedError

        elif option2 == "FromFeatures":
            raise NotImplementedError

    elif option1 == "FromFile":
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
