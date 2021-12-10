from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFcablemesh_modify_nodes"


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

    cablemesh.settings['show.vertices:free'] = True
    scene.update()

    options = ["AllBoundaryNodes", "Corners", "ByContinuousEdges", "Manual"]

    option = compas_rhino.rs.GetString("Selection mode:", strings=options).lower()

    if not option:
        return

    if option == "allboundarynodes":
        keys = cablemesh.datastructure.vertices_on_boundary()

    elif option == "corners":
        angle = compas_rhino.rs.GetInteger('Angle tolerance for non-quad face corners:', 170, 1, 180)
        keys = cablemesh.datastructure.corner_vertices(tol=angle)

    elif option == "bycontinuousedges":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.vertices_on_edge_loop(key) for key in temp])))

    elif option == "manual":
        keys = cablemesh.select_vertices()

    if keys:
        public = [name for name in cablemesh.datastructure.default_vertex_attributes.keys() if not name.startswith('_')]
        if cablemesh.update_vertices_attributes(keys, names=public):
            cablemesh.settings['_is.valid'] = False
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
