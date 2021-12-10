from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFcablemesh_modify_edges"


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

    options = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options).lower()

    if not option:
        return

    if option == "all":
        keys = keys = list(cablemesh.datastructure.edges())

    elif option == "allboundaryedges":
        keys = cablemesh.datastructure.edges_on_boundary()

    elif option == "continuous":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.edge_loop(key) for key in temp])))

    elif option == "parallel":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.edge_strip(key) for key in temp])))

    elif option == "manual":
        keys = cablemesh.select_edges()

    if keys:
        public = [name for name in cablemesh.datastructure.default_edge_attributes.keys() if not name.startswith('_')]
        if cablemesh.update_edges_attributes(keys, names=public):
            cablemesh.settings['_is.valid'] = False
            if scene.settings['FF']['autoupdate']:
                FFsolve_fd_cmd.RunCommand(True)
            else:
                scene.update()
        compas_rhino.rs.UnselectAllObjects()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
