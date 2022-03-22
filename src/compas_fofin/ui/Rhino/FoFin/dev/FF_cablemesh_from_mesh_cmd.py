from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.conversions import RhinoMesh

from compas_ui.app import App
from compas_fofin.datastructures import CableMesh


__commandname__ = 'FF_cablemesh_from_mesh'


@App.error()
def RunCommand(is_interactive):

    app = App()

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    mesh = RhinoMesh.from_guid(guid).to_compas(cls=CableMesh)
    mesh.name = 'CableMesh'

    app.scene.clear()
    app.scene.add(mesh, name=mesh.name)
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
