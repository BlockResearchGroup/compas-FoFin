from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_modify_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    cablemesh.settings["show.vertices:anchors"] = True
    cablemesh.settings["show.vertices:free"] = True

    cablemesh.is_valid = False

    ui.scene.update()

    nodes = ui.controller.mesh_select_vertices(cablemesh)

    if nodes:
        public = [
            name
            for name in cablemesh.mesh.default_vertex_attributes.keys()
            if not name.startswith("_")
        ]
        cablemesh.modify_vertices(nodes, names=public)

    cablemesh.settings["show.vertices:anchors"] = True
    cablemesh.settings["show.vertices:free"] = False

    ui.scene.update()
    ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
