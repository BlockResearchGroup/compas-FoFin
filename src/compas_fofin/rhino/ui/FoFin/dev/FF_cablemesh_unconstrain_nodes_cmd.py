from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_unconstrain_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    nodes = ui.controller.mesh_select_vertices(cablemesh)

    if nodes:
        for node in nodes:
            cablemesh.mesh.unset_vertex_attribute(node, "constraint")

        cablemesh.is_valid = False
        ui.scene.update()
        ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
