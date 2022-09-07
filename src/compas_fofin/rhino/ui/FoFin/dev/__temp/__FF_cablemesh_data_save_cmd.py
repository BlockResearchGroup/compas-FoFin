from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_data_save"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    path = ui.pick_file_save("FoFin.data")
    if path:
        compas.json_dump(mesh, path)


if __name__ == "__main__":
    RunCommand(True)
