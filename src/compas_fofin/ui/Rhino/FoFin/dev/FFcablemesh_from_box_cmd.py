from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_fofin.datastructures import CableMesh
from compas_rhino.geometry import RhinoBox
from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_from_box"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_object('Select a box.')
    if not guid:
        return

    sub = compas_rhino.rs.GetInteger("Number of levels of subdivision:", 2, 0, 20)
    if not sub or sub is None:
        scene.update()
        return

    box = RhinoBox.from_guid(guid).to_compas()
    mesh = CableMesh.from_shape(box)
    cablemesh = mesh.subdivide(scheme='quad', k=sub)

    compas_rhino.rs.HideObject(guid)

    scene.clear()
    scene.add(cablemesh, name='cablemesh')
    scene.update()

    print("CableMesh object successfully created. Input box has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
