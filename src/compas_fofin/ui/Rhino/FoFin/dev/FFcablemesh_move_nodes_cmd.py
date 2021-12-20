from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


import FFsolve_fd_cmd


__commandname__ = "FFcablemesh_move_nodes"


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

    key = cablemesh.select_vertex()

    if key is not None:
        if cablemesh.datastructure.vertex_attribute(key, 'constraint'):
            constraint = cablemesh.datastructure.vertex_attribute(key, 'constraint')
            move = cablemesh.move_vertex_constraint(key, constraint)

        else:
            mdir_options = ["Free", "X", "Y", "Z", "XY", "YZ", "ZX"]
            mdir = compas_rhino.rs.GetString("Set Direction.", strings=mdir_options)
            if not mdir or mdir is None:
                mdir = 'free'

            mdir = mdir.lower()
            if mdir == 'free':
                move = cablemesh.move_vertices([key])
            else:
                move = cablemesh.move_vertices_direction([key], direction=mdir)

        if move:
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
