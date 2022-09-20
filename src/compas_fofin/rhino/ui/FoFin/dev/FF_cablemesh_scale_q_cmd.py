from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    cablemesh.settings["show.edges"] = True
    ui.scene.update()

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    options = ["Value", "Interactive"]
    mode = ui.get_string(message="Scaling mode?", options=options)
    if not mode:
        return

    selected = ui.controller.mesh_select_edges(cablemesh)
    if not selected:
        return

    # this should be a cloud call with cached values
    # anchors, edges, loads, ... are constant
    # only Q needs to be sent
    # and new (free) vertex locations should be received

    Q = cablemesh.mesh.edges_attribute("q", keys=selected)

    if mode == "Value":
        scale = ui.get_real("Scaling factor?", minval=-1e2, maxval=+1e2, default=1.0)

    elif mode == "Interactive":
        # start the dynamic scaling process

        cablemesh.is_valid = False
        ui.scene.update()

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Base point for scaling.")

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        o = gp.Point()

        gp.SetCommandPrompt("Reference point 1.")
        gp.SetBasePoint(o, False)
        gp.DrawLineFromPoint(o, True)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        r1 = gp.Point()
        v1 = r1 - o
        l1 = v1.SquareLength

        def OnDynamicDraw(sender, e):
            cablemesh.clear_conduits()

            r2 = e.CurrentPoint
            v2 = r2 - o
            l2 = v2.SquareLength

            sign = +1 if Rhino.Geometry.Vector3d.Multiply(v1, v2) > 0 else -1
            scale = sign * l2 / l1

            for edge, q in zip(selected, Q):
                cablemesh.mesh.edge_attribute(edge, "q", q * scale)

            # replace this by a call with cached values
            # cached: anchors, edges, loads
            # sent: q
            # received: xyz
            cablemesh.update_equilibrium(ui)
            cablemesh._draw_force_overlays()
            cablemesh._draw_reaction_overlays()

        gp.SetCommandPrompt("Reference point 2.")
        gp.SetBasePoint(o, False)
        gp.DrawLineFromPoint(o, True)
        gp.Constrain(Rhino.Geometry.Line(o, r1))
        gp.DynamicDraw += OnDynamicDraw

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        r2 = gp.Point()
        v2 = r2 - o
        l2 = v2.SquareLength

        sign = +1 if Rhino.Geometry.Vector3d.Multiply(v1, v2) > 0 else -1
        scale = sign * l2 / l1

    if scale is not None:
        for edge, q in zip(selected, Q):
            cablemesh.mesh.edge_attribute(edge, "q", q * scale)

        cablemesh.update_equilibrium(ui)

    else:
        cablemesh.is_valid = False

    ui.scene.update()
    ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
