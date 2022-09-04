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

    edges = ui.controller.mesh_select_edges(cablemesh)
    if not edges:
        return

    scale = ui.get_real("Scale factor?", minval=-1e3, maxval=1e3, default=1.0)

    if scale:
        Q = cablemesh.mesh.edges_attribute("q", keys=edges)
        Q = [q * scale for q in Q]
        for edge, q in zip(edges, Q):
            cablemesh.mesh.edge_attribute(edge, "q", q)
        cablemesh.is_valid = False
        ui.scene.update()
        ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
