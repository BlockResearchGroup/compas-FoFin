from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.conversions import RhinoMesh

from compas.datastructures import mesh_weld

from compas_ui.ui import UI
from compas_ui.rhino.callbacks import register_callback

from compas_fofin.datastructures import CableMesh

from callbacks import FF_on_object_update


__commandname__ = "FF_cablemesh_from_mesh"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    mesh = RhinoMesh.from_guid(guid).to_compas(cls=CableMesh)
    mesh = mesh_weld(mesh)
    mesh.name = "CableMesh"

    compas_rhino.rs.HideObject(guid)
    ui.scene.add(mesh, name=mesh.name)
    ui.scene.update()
    ui.record()

    register_callback(FF_on_object_update)


if __name__ == "__main__":
    RunCommand(True)
