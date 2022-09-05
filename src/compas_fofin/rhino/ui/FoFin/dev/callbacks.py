from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


def FF_on_object_update(*args):
    """
    Callback for the "ReplaceRhinoObject" event.

    Parameters
    ----------
    *args : tuple

    Returns
    -------
    None

    """
    ui = UI()

    e = args[1]
    obj = e.NewRhinoObject

    # - Update geometry (when boundary nodes are moved)
    # - Update constraints (when constraint objects are modified)

    cablemesh = ui.scene.active_object
    if not isinstance(cablemesh, CableMeshObject):
        return

    # only trigger as redraw if there is something to redraw
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

    # if the active cablemesh was affected by the Rhino object changes
    # the scene should be redrawn
    if is_dirty:
        cablemesh.is_valid = False
        ui.scene.update()
        print("all should be well...")
