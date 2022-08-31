from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_unconstrain_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]
    nodes = ui.controller.mesh_select_vertices(cablemesh)

    if nodes:
        for node in nodes:
            cablemesh.mesh.unset_vertex_attribute(node, "constraint")
        ui.scene.update()
        ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
