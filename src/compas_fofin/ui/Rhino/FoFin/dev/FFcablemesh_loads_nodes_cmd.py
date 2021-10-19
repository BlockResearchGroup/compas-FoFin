from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_loads_nodes"


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

    # show also free vertices
    cablemesh.settings['show.vertices:free'] = True
    scene.update()

    options = ["AllBoundaryNodes", "Corners", "ByContinuousEdges", "Manual"]

    option = compas_rhino.rs.GetString("Selection mode:", strings=options)

    if not option:
        return

    if option == "AllBoundaryNodes":
        keys = cablemesh.datastructure.vertices_on_boundary()

    elif option == "Corners":
        angle = compas_rhino.rs.GetInteger('Angle tolerance for non-quad face corners:', 170, 1, 180)
        keys = cablemesh.datastructure.corner_vertices(tol=angle)

    elif option == "ByContinuousEdges":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.vertices_on_edge_loop(key) for key in temp])))

    elif option == "Manual":
        keys = cablemesh.select_vertices()

    if keys:
        public = ['px', 'py', 'pz']
        if cablemesh.update_vertices_attributes(keys, names=public):
            cablemesh.settings['_is.valid'] = False
            cablemesh.settings['show.vertices:free'] = False
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
