from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms import MeshDataForm
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_data"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    form = MeshDataForm(
        mesh,
        excluded_vertex_attr=("constraint", "param"),
        excluded_edge_attr=("_is_edge"),
        excluded_face_attr=("is_loaded"),
    )

    if form.show():
        ui.scene.update()
        ui.record()


if __name__ == "__main__":
    RunCommand(True)
