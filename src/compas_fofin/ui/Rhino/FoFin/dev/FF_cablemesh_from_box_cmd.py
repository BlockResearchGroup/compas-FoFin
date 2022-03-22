from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.conversions import RhinoBox
from compas_ui.app import App

from compas_fofin.datastructures import CableMesh


__commandname__ = 'FF_cablemesh_from_box'


@App.error()
def RunCommand(is_interactive):

    app = App()

    guid = compas_rhino.select_object("Select a box.")
    if not guid:
        return

    k = app.get_integer("Resolution?", minval=1, maxval=6, default=2)
    if not k:
        return

    box = RhinoBox.from_guid(guid).to_compas()

    mesh = CableMesh.from_shape(box)
    mesh = mesh.subdivide(scheme='quad', k=k)
    mesh.name = 'CableMesh'

    compas_rhino.rs.HideObject(guid)
    app.scene.clear()
    app.scene.add(mesh, name=mesh.name)
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
