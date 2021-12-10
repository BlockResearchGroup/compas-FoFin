from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFcablemesh_modify_edges_qs"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    current_setting = cablemesh.settings['show.pipes:forcedensities']

    # ==========================================================================
    # select edges
    # ==========================================================================

    options1 = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]

    while True:
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

        # ==========================================================================
        # modify qs
        # ==========================================================================

        cablemesh.settings['show.pipes:forcedensities'] = True
        scene.update()

        if keys:

            text = {edge: cablemesh.datastructure.edge_attribute(edge, 'q') for edge in keys}

            cablemesh.artist.draw_edgelabels(text=text)
            compas_rhino.rs.EnableRedraw()

            options2 = ["Interactive", "ScaleCurrent", "AssignNew"]
            option2 = compas_rhino.rs.GetString("Modify force densities", strings=options2)

            if not option2:
                scene.update()
                break

            if option2 == "Interactive":
                print('This feature is not implemented yet.')
                scene.update()
                break

            elif option2 == "ScaleCurrent":
                scale = compas_rhino.rs.GetReal("Enter scale")
                if scale:
                    for edge in keys:
                        q = cablemesh.datastructure.edge_attribute(edge, 'q')
                        cablemesh.datastructure.edge_attribute(edge, 'q', q * scale)
                    FFsolve_fd_cmd.RunCommand(True)

            elif option2 == "AssignNew":
                scale = compas_rhino.rs.GetReal("Enter new force density")
                if scale:
                    cablemesh.datastructure.edges_attribute('q', scale, keys)
                    FFsolve_fd_cmd.RunCommand(True)

            scene.update()

    cablemesh.settings['show.pipes:forcedensities'] = current_setting
    scene.update()
