import os
import json
from compas.plugins import plugin
from compas_ui.ui import UI
from compas_ui.rhino.callbacks import register_callback
from compas_fofin.rhino.install import plugin_devpath
from compas_fofin.rhino.objects import RhinoCableMeshObject


@plugin(category="ui")
def register(ui):

    # register settings
    devpath = plugin_devpath("FoFin")
    configpath = os.path.join(devpath, "config.json")
    with open(configpath, "r") as f:
        config = json.load(f)
        settings = config["settings"]
        ui.settings["FoFin"] = settings

    # register callbacks
    register_callback(FF_on_object_update)


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
    if not isinstance(cablemesh, RhinoCableMeshObject):
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