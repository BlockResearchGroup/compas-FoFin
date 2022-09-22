from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from compas_ui.ui import UI
from compas_ui.rhino.forms import ToolbarForm


__commandname__ = "FF_toolbar"


HERE = os.path.dirname(__file__)


@UI.error()
def RunCommand(is_interactive):

    config = [
        {
            "command": "FF_toolbar_cablemesh_create",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_create.png"),
        },
        {
            "command": "FF_cablemesh_anchors",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_anchors.png"),
        },
        {
            "command": "FF_cablemesh_solve_fd",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_solve_fd.png"),
        },
        {"type": "separator"},
        {
            "command": "FF_cablemesh_move_nodes",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_move_nodes.png"),
        },
        {
            "command": "FF_cablemesh_constrain_nodes",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_constrain_nodes.png"),
        },
        {
            "command": "FF_cablemesh_update_constraints",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_update_constraints.png"),
        },
        {
            "command": "FF_cablemesh_scale_q",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_scale_q.png"),
        },
        {"type": "separator"},
        {
            "command": "FF_cablemesh_modify_nodes",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_modify_nodes.png"),
        },
        {
            "command": "FF_cablemesh_modify_edges",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_modify_edges.png"),
        },
        {"type": "separator"},
        {
            "command": "FF_cablemesh_edges_delete",
            "icon": os.path.join(HERE, "assets", "FF_cablemesh_edges_delete.png"),
        },
    ]

    toolbar = ToolbarForm()
    toolbar.setup(config, HERE, title="FormFinder")
    toolbar.Show()


if __name__ == "__main__":
    RunCommand(True)
