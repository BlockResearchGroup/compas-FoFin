from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb

from compas.geometry import distance_point_point
from compas.geometry import scale_vector
from compas.geometry import length_vector_sqrd
from compas.geometry import add_vectors

from compas.utilities import flatten
from compas.utilities import i_to_blue
from compas.utilities import i_to_red

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import get_proxy
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd

import Rhino

from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

from Rhino.ApplicationSettings import ModelAidSettings


__commandname__ = "FFcablemesh_modify_edges_qs"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    mesh_fd = proxy.function('compas_fd.fd.mesh_fd_constrained_numpy')

    current_setting = cablemesh.settings['show.pipes:forcedensities']

    # ==========================================================================
    # select edges
    # ==========================================================================

    options1 = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]

    while True:

        cablemesh.settings['show.pipes:forcedensities'] = True
        scene.update()

        option1 = compas_rhino.rs.GetString("Selection Type", strings=options1)

        if option1 is None:
            scene.update()
            break

        if not option1:
            scene.update()
            break

        if option1 == "All":
            keys = keys = list(cablemesh.datastructure.edges())

        elif option1 == "AllBoundaryEdges":
            keys = cablemesh.datastructure.edges_on_boundary()

        elif option1 == "Continuous":
            temp = cablemesh.select_edges()
            keys = list(set(flatten([cablemesh.datastructure.edge_loop(key) for key in temp])))

        elif option1 == "Parallel":
            temp = cablemesh.select_edges()
            keys = list(set(flatten([cablemesh.datastructure.edge_strip(key) for key in temp])))

        elif option1 == "Manual":
            keys = cablemesh.select_edges()

        # ======================================================================
        # modify qs
        # ======================================================================

        if keys:

            color = {}
            edges = list(cablemesh.datastructure.edges())
            qs = {edge: cablemesh.datastructure.edge_attribute(edge, 'q') for edge in edges}
            qmin = min(qs.values())
            qmax = max(qs.values())

            for edge in edges:
                if qs[edge] >= 0.0:
                    color[edge] = i_to_red((qs[edge]) / qmax)
                elif qs[edge] < 0.0:
                    color[edge] = i_to_blue((qs[edge]) / qmin)

            text = {}
            for u, v in keys:
                if (u, v) not in qs:
                    u, v = v, u
                text[(u, v)] = round(qs[(u, v)], 2)

            cablemesh.artist.draw_edgelabels(text=text, color=color)
            compas_rhino.rs.EnableRedraw()

            options2 = ["Interactive", "ScaleCurrent", "AssignNew"]
            option2 = compas_rhino.rs.GetString("Modify force densities", strings=options2)

            if not option2:
                scene.update()
                break

            # ==================================================================
            # 1. interactive
            # ==================================================================

            if option2 == "Interactive":

                ip = Rhino.Input.Custom.GetPoint()
                ip.SetCommandPrompt("select base point")
                ip.Get()
                ip = ip.Point()

                cablemesh.conduit_reactions.disable()
                cablemesh.conduit_pipes_q.disable()
                cablemesh.conduit_pipes_q.values = {edge: 0.0 for edge in cablemesh.datastructure.edges()}
                cablemesh.conduit_pipes_q.color = {edge: (150, 150, 150) for edge in cablemesh.datastructure.edges()}
                cablemesh.conduit_pipes_q.enable()
                cablemesh.artist.clear()

                cablemesh.artist.draw_edgelabels(text=text, color=(150, 150, 150))
                compas_rhino.rs.EnableRedraw()

                # ==============================================================
                # dynamic draw
                # ==============================================================

                def OnDynamicDraw(sender, e):

                    cp = e.CurrentPoint

                    scale = distance_point_point(ip, cp)

                    if scale < 0.1:
                        scale = 0.1
                    if scale > 20.0:
                        scale = 20.0

                    for edge in keys:
                        cablemesh.datastructure.edge_attribute(edge, 'q', scale)

                    # draw edges -----------------------------------------------

                    if (len(list(cablemesh.datastructure.faces()))) > 2000:
                        print('More than 2000 faces... dynamic draw has been turned off!')
                    else:
                        result = mesh_fd(cablemesh.datastructure)
                        cablemesh.datastructure.data = result.data

                    edges = list(cablemesh.datastructure.edges())
                    color = {edge: (0, 0, 0) for edge in edges}
                    qs = {edge: cablemesh.datastructure.edge_attribute(edge, 'q') for edge in edges}

                    qmin = min(qs.values())
                    qmax = max(qs.values())
                    q_range = qmax - qmin or 1

                    for edge in edges:
                        if qs[edge] >= 0.0:
                            color[edge] = i_to_red((qs[edge]) / qmax)
                        elif qs[edge] < 0.0:
                            color[edge] = i_to_blue((qs[edge]) / qmin)

                    tmin = cablemesh.settings['pipe_thickness.min']
                    tmax = cablemesh.settings['pipe_thickness.max']
                    t_range = tmax - tmin

                    qs_remapped = {edge: (((q - qmin) * t_range) / q_range) + tmin for edge, q in qs.iteritems()}

                    for edge in edges:
                        u_xyz = Point3d(*cablemesh.datastructure.vertex_coordinates(edge[0]))
                        v_xyz = Point3d(*cablemesh.datastructure.vertex_coordinates(edge[1]))
                        e.Display.DrawLine(Line(u_xyz, v_xyz), FromArgb(*color[edge]), int(abs(qs_remapped[edge])))

                    # reactions ------------------------------------------------
                    r_color = cablemesh.settings['color.reactions']
                    r_scale = cablemesh.settings['scale.externalforces']
                    r_tol = cablemesh.settings['tol.externalforces']
                    for vertex in cablemesh.datastructure.vertices():
                        ep = cablemesh.datastructure.vertex_coordinates(vertex)
                        r = cablemesh.datastructure.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
                        r = scale_vector(r, -r_scale)
                        if length_vector_sqrd(r) < r_tol ** 2:
                            continue
                        sp = add_vectors(ep, r)
                        line = Line(Point3d(*ep), Point3d(*sp))
                        e.Display.DrawArrow(line,
                                            FromArgb(*r_color),
                                            0,
                                            0.1)

                    # dots -----------------------------------------------------
                    for edge in keys:
                        if edge not in edges:
                            edge = edge[1], edge[0]
                        mp = cablemesh.datastructure.edge_midpoint(edge[0], edge[1])
                        dot = Rhino.Geometry.TextDot(str(round(scale, 2)), Point3d(*mp))
                        dot.FontHeight = 10
                        dot.FontFace = 'Arial Regular'
                        e.Display.DrawDot(dot, FromArgb(*color[edge]), FromArgb(0, 0, 0), FromArgb(*color[edge]))

                # ==============================================================
                # get target point
                # ==============================================================

                ModelAidSettings.Ortho = True
                gp = Rhino.Input.Custom.GetPoint()
                gp.DrawLineFromPoint(ip, True)
                gp.SetCommandPrompt("select end point")
                gp.DynamicDraw += OnDynamicDraw
                gp.Get()
                gp = gp.Point()

                scale = distance_point_point(ip, gp)
                if scale < 0.1:
                    scale = 0.1
                if scale > 20.0:
                    scale = 20.0

                # ==============================================================
                # update
                # ==============================================================

                for edge in keys:
                    q = cablemesh.datastructure.edge_attribute(edge, 'q')
                    cablemesh.datastructure.edge_attribute(edge, 'q', scale)

                result = mesh_fd(cablemesh.datastructure)
                cablemesh.datastructure.data = result.data

            # ==================================================================
            # 2. scale
            # ==================================================================

            elif option2 == "ScaleCurrent":
                scale = compas_rhino.rs.GetReal("Enter scale")
                if scale:
                    for edge in keys:
                        q = cablemesh.datastructure.edge_attribute(edge, 'q')
                        cablemesh.datastructure.edge_attribute(edge, 'q', q * scale)
                    FFsolve_fd_cmd.RunCommand(True)

            # ==================================================================
            # 3. assign new
            # ==================================================================

            elif option2 == "AssignNew":
                scale = compas_rhino.rs.GetReal("Enter new force density")
                if scale:
                    cablemesh.datastructure.edges_attribute('q', scale, keys)
                    FFsolve_fd_cmd.RunCommand(True)

            scene.update()

    cablemesh.settings['show.pipes:forcedensities'] = current_setting
    scene.update()
