from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_anchors"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]
    mesh = cablemesh.mesh

    fixed = list(mesh.vertices_where(is_fixed=True))
    leaves = list(mesh.vertices_where(vertex_degree=1))
    vertices = list(set(fixed + leaves))

    if vertices:
        mesh.vertices_attribute("is_anchor", True, keys=vertices)

    options = ["Select", "Unselect"]
    option = ui.get_string("Select/Unselect anchors.", options=options)
    if not option:
        return

    is_anchor = option == "Select"

    while True:
        compas_rhino.rs.UnselectAllObjects()
        cablemesh.settings["show.vertices:free"] = True
        ui.scene.update()

        nodes = ui.controller.mesh_select_vertices(cablemesh)
        if not nodes:
            break

        cablemesh.is_valid = False
        mesh.vertices_attribute("is_anchor", is_anchor, keys=nodes)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.settings["show.vertices:free"] = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
