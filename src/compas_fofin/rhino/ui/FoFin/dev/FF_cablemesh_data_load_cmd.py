from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject
from compas_fofin.datastructures import CableMesh


__commandname__ = "FF_cablemesh_data_load"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    path = ui.pick_file_open()
    if path:
        mesh = compas.json_load(path)
        name = cablemesh.name
        settings = cablemesh.settings.copy()
        ui.scene.clear()
        ui.scene.add(CableMesh.from_data(mesh.data), name=name, settings=settings)
        ui.scene.update()
        ui.record()


if __name__ == "__main__":
    RunCommand(True)
