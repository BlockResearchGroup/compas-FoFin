from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]

    edges = ui.controller.mesh_select_edges(cablemesh)

    if edges:
        public = [
            name
            for name in cablemesh.mesh.default_edge_attributes.keys()
            if not name.startswith("_")
        ]
        if cablemesh.modify_edges(edges, names=public):
            cablemesh.is_valid = False
            ui.scene.update()
            ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
