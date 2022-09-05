from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_update_constraints"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    cablemesh.update_constraints()

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
