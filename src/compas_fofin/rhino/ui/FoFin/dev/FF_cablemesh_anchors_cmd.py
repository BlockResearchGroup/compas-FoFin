from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_anchors"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    fixed = list(mesh.vertices_where(is_fixed=True))
    leaves = list(mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        mesh.vertices_attribute("is_anchor", True, keys=vertices)

    options = ["Select", "Unselect"]
    option = ui.get_string("Select/Unselect anchors", options=options)
    if not option:
        return

    is_anchor = option == "Select"
    cablemesh.settings["show.vertices:free"] = option == "Select"

    cablemesh.is_valid = False

    while True:
        compas_rhino.rs.UnselectAllObjects()
        ui.scene.update()

        nodes = ui.controller.mesh_select_vertices(cablemesh)
        if not nodes:
            break

        mesh.vertices_attribute("is_anchor", is_anchor, keys=nodes)
        if not is_anchor:
            for node in nodes:
                mesh.unset_vertex_attribute(node, "constraint")

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.settings["show.vertices:free"] = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
