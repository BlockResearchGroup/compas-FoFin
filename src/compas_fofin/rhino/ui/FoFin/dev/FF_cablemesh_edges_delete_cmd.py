from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_edges_delete"


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
        fkeys = set()
        for (u, v) in edges:
            fkeys.update(cablemesh.mesh.edge_faces(u, v))
        for fkey in fkeys:
            if fkey:
                cablemesh.mesh.delete_face(fkey)

        cablemesh.mesh.remove_unused_vertices()
        ui.scene.update()
        ui.record()

    ui.scene.update()
    ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
