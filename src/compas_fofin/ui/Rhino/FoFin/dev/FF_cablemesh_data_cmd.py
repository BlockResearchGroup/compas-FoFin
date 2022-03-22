from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms import MeshDataForm
from compas_ui.app import App


__commandname__ = "FF_cablemesh_data"


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    form = MeshDataForm(mesh,
                        excluded_vertex_attr=('constraint', 'param'),
                        excluded_edge_attr=('_is_edge'),
                        excluded_face_attr=('is_loaded'))

    if form.show():
        app.scene.update()
        app.record()


if __name__ == "__main__":
    RunCommand(True)
