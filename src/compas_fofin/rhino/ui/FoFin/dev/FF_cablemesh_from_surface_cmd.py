from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rhino.conversions import RhinoSurface
from compas_fofin.datastructures import CableMesh


__commandname__ = "FF_cablemesh_from_surface"


@UI.error()
def RunCommand(is_interactive):
    ui = UI()

    guid = compas_rhino.select_surface()
    if not guid:
        return

    U = ui.get_integer(
        "Number of faces in the U direction",
        minval=1,
        maxval=1000,
        default=10,
    )
    if not U:
        return

    V = ui.get_integer(
        "Number of faces in the V direction",
        minval=1,
        maxval=1000,
        default=U,
    )
    if not V:
        return

    mesh = RhinoSurface.from_guid(guid).to_compas_quadmesh(
        nu=U,
        nv=V,
        weld=True,
        cls=CableMesh,
    )
    mesh.name = "CableMesh"

    compas_rhino.rs.HideObject(guid)
    ui.scene.add(mesh, name=mesh.name)
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
