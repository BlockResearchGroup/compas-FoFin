from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFcablemesh_anchors"


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

    # mark all fixed vertices as anchors
    # mark all leaves as anchors

    fixed = list(cablemesh.datastructure.vertices_where({'is_fixed': True}))
    leaves = []
    for vertex in cablemesh.datastructure.vertices():
        nbrs = cablemesh.datastructure.vertex_neighbors(vertex)
        count = 0
        for nbr in nbrs:
            if cablemesh.datastructure.edge_attribute((vertex, nbr), '_is_edge'):
                count += 1
        if count == 1:
            leaves.append(vertex)

    anchors = list(set(fixed) | set(leaves))
    if anchors:
        cablemesh.datastructure.vertices_attribute('is_anchor', True, keys=anchors)
        print("Fixed nodes of the CableMesh have automatically been defined as supports.")
        scene.update()

    options = ["Select", "Unselect"]
    option1 = compas_rhino.rs.GetString("Select or unselect nodes as supports:", strings=options)
    if not option1 or option1 is None:
        scene.update()
        return
    option1 = option1.lower()

    options = ["AllBoundaryNodes", "Corners", "ByContinuousEdges", "Manual"]

    while True:
        option2 = compas_rhino.rs.GetString("Selection mode:", strings=options)

        if not option2 or option2 is None:
            compas_rhino.rs.UnselectAllObjects()
            cablemesh.settings['show.vertices:free'] = False
            scene.update()
            return
        option2 = option2.lower()

        if option2 == "allboundarynodes":
            keys = list(set(flatten(cablemesh.datastructure.vertices_on_boundaries())))

        elif option2 == "corners":
            keys = cablemesh.datastructure.corner_vertices()

        elif option2 == "bycontinuousedges":
            edges = cablemesh.select_edges()
            keys = list(set(flatten([cablemesh.datastructure.vertices_on_edge_loop(edge) for edge in edges])))

        elif option2 == "manual":
            cablemesh.settings['show.vertices:free'] = True
            scene.update()
            keys = cablemesh.select_vertices()

        if keys:
            cablemesh.settings['_is.valid'] = False
            if option1 == "select":
                cablemesh.datastructure.vertices_attribute('is_anchor', True, keys=keys)
            else:
                cablemesh.datastructure.vertices_attribute('is_anchor', False, keys=keys)

        compas_rhino.rs.UnselectAllObjects()
        cablemesh.settings['show.vertices:free'] = False
        if scene.settings['FF']['autoupdate']:
            FFsolve_fd_cmd.RunCommand(True)
        else:
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
