from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    cablemesh.is_valid = False
    ui.scene.update()

    edges = ui.controller.mesh_select_edges(cablemesh)

    if edges:

        public = [
            name
            for name in cablemesh.mesh.default_edge_attributes.keys()
            if not name.startswith("_")
        ]
        cablemesh.modify_edges(edges, names=public)

    ui.scene.update()
    ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
