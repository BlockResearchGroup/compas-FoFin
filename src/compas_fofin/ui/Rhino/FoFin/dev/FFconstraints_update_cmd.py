from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


import FFsolve_fd_cmd


__commandname__ = "FFconstraints_update"


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

    constraints = cablemesh.datastructure.vertices_attribute('constraint')
    constraints = list(filter(None, constraints))
    if not constraints:
        print('There are no constraints in this CableMesh.')
        return

    for key in cablemesh.datastructure.vertices():
        if cablemesh.datastructure.vertex_attribute(key, 'constraint'):
            constraint = cablemesh.datastructure.vertex_attribute(key, 'constraint')
            constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')

            constraint.compute_param()
            constraint.update_geometry_guid()
            constraint.update_location_at_param()

            cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)

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
