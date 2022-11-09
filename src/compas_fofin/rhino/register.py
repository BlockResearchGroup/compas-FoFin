import os
from compas.plugins import plugin
from compas_ui.ui import UI

from compas_fofin.rhino.objects import RhinoCableMeshObject

from compas_ui.values import Settings
from compas_ui.values import BoolValue
from compas_ui.values import IntValue
from compas_ui.values import FloatValue


HERE = os.path.dirname(__file__)

SETTINGS = Settings(
    {
        "solver.autorun": BoolValue(True),
        "solver.show_iterations": BoolValue(False),
        "solver.kmax": IntValue(100),
        "solver.damping": FloatValue(0.1),
        "solver.tol.residuals": FloatValue(1e-3),
        "solver.tol.displacements": FloatValue(1e-3),
    }
)


@plugin(category="ui")
def register(ui):

    plugin_name = "FoFin"
    plugin_path = os.path.join(HERE, "ui", plugin_name)
    if not os.path.isdir(plugin_path):
        raise Exception("Cannot find the plugin: {}".format(plugin_path))

    ui.registry["FoFin"] = SETTINGS


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
