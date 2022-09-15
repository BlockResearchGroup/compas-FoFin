from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_edges_delete"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]
    mesh = cablemesh.mesh

    edges = ui.controller.mesh_select_edges(cablemesh)

    if edges:
        fkeys = set()
        for (u, v) in edges:
            fkeys.update(mesh.edge_faces(u, v))
        for fkey in fkeys:
            if fkey:
                mesh.delete_face(fkey)

        mesh.remove_unused_vertices()
        cablemesh.is_valid = False
        ui.scene.update()
        ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
