from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


def FF_on_object_update(*args):
    ui = UI()

    e = args[1]
    obj = e.NewRhinoObject

    cablemesh = ui.scene.active_object
    if not isinstance(cablemesh, CableMeshObject):
        return

    is_dirty = False

    for vertex in cablemesh.mesh.vertices_where(is_anchor=True):
        # using the active cablemesh
        # check if any of the vertex constraints corresponds to the changed object
        constraint = cablemesh.mesh.vertex_attribute(vertex, "constraint")
        if not constraint:
            continue

        # update the vertex constraint
        cablemesh.update_constraint(vertex, constraint, obj)

        # mark the cablemesh for redrawing
        is_dirty = True

    if is_dirty:
        cablemesh.is_valid = False
        ui.scene.update()
        print("all should be well...")
