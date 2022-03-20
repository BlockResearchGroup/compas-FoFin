from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms import MeshForm
from compas_ui.rhino.forms import error
from compas_ui.app import App


__commandname__ = "FF_cablemesh_modify"


@error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    form = MeshForm(mesh)
    form.show()


if __name__ == "__main__":
    RunCommand(True)
