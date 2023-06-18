from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_scale_q"


@UI.error()
def RunCommand(is_interactive):
    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    options = ["Value", "Interactive"]
    mode = ui.get_string(message="Scaling mode", options=options)
    if not mode:
        return

    cablemesh.is_valid = False
    ui.scene.update()

    selected = ui.controller.mesh_select_edges(cablemesh)
    if not selected:
        return

    Q = cablemesh.mesh.edges_attribute("q", keys=selected)

    if mode == "Value":
        scale = ui.get_real("Scaling factor", minval=-1e2, maxval=+1e2, default=1.0)

    elif mode == "Interactive":
        fd_create = ui.proxy.function("compas_fd.fd.mesh_fd_constrained_cache_create", cache=True)
        fd_call = ui.proxy.function("compas_fd.fd.mesh_fd_constrained_cache_call")
        fd_delete = ui.proxy.function("compas_fd.fd.mesh_fd_constrained_cache_delete")

        cached_data = fd_create(
            cablemesh.mesh,
            selected,
            kmax=ui.registry["FoFin"]["solver.kmax"],
            damping=ui.registry["FoFin"]["solver.damping"],
            tol_res=ui.registry["FoFin"]["solver.tol.residuals"],
            tol_disp=ui.registry["FoFin"]["solver.tol.displacements"],
        )

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Base point for scaling")

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        base = gp.Point()

        gp.SetCommandPrompt("Reference point 1")
        gp.SetBasePoint(base, False)
        gp.DrawLineFromPoint(base, True)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        ref1 = gp.Point()
        vec1 = ref1 - base
        l1 = vec1.SquareLength

        def OnDynamicDraw(sender, e):
            cablemesh.conduit_edges.disable()

            ref2 = e.CurrentPoint
            vec2 = ref2 - base
            l2 = vec2.SquareLength

            sign = +1 if Rhino.Geometry.Vector3d.Multiply(vec1, vec2) > 0 else -1
            scale = sign * l2 / l1
            xyz = fd_call(scale, cached_data)

            cablemesh.conduit_edges.xyz = xyz
            cablemesh.conduit_edges.enable()

        gp.SetCommandPrompt("Reference point 2")
        gp.SetBasePoint(base, False)
        gp.DrawLineFromPoint(base, True)
        gp.Constrain(Rhino.Geometry.Line(base, ref1))
        gp.DynamicDraw += OnDynamicDraw

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            for edge, q in zip(selected, Q):
                cablemesh.mesh.edge_attribute(edge, "q", q)
            cablemesh.update_equilibrium(ui)

        ref2 = gp.Point()
        vec2 = ref2 - base
        l2 = vec2.SquareLength

        sign = +1 if Rhino.Geometry.Vector3d.Multiply(vec1, vec2) > 0 else -1
        scale = sign * l2 / l1
        print(scale)

        fd_delete()
        cablemesh.conduit_edges.disable()

    if scale is None:
        cablemesh.is_valid = False
    else:
        for edge, q in zip(selected, Q):
            cablemesh.mesh.edge_attribute(edge, "q", q * scale)
        cablemesh.update_equilibrium(ui)

    ui.scene.update()
    ui.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
