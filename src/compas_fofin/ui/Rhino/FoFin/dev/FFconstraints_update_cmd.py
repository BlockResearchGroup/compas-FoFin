from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Vector, Frame
from compas.geometry import Line, Plane
from compas_rhino.geometry import RhinoNurbsCurve

import compas_rhino

from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
# from compas_rhino.geometry import RhinoSurface

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


import FFsolve_fd_cmd

import System


__commandname__ = "FFconstraints_update"


def line_point_at(line, param):  # Tom
    d = line.direction
    pt = line.start + d * param
    return pt


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    print('yess')

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    for key in cablemesh.datastructure.vertices():
        print(cablemesh.datastructure.vertex_attribute(key, 'constraint'))
        if cablemesh.datastructure.vertex_attribute(key, 'constraint'):
            constraint = cablemesh.datastructure.vertex_attribute(key, 'constraint')
            if type(constraint.geometry) in [Vector, Frame]:
                continue

            constraint.guid = System.Guid(constraint.guid)
            guid = constraint.guid
            print('yes')

            if type(constraint.geometry) == Line:

                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.compute_param()  # Tom

                rhinoLine = RhinoLine.from_guid(guid)
                print(rhinoLine.object)
                constraint.geometry = rhinoLine.to_compas()
                constraint.location = line_point_at(constraint.geometry, constraint.param)

            elif type(constraint.geometry) == Plane:
                constraint.compute_param()  # Tom > plane has no direction > intermediate frame?!

                line = RhinoLine.from_guid(guid).to_compas()
                constraint.geometry = Plane(line.start, line.vector)

            elif type(constraint.geometry) == RhinoNurbsCurve:
                constraint.geometry = RhinoCurve.from_guid(guid).to_compas()
                constraint.location = constraint.geometry.point_at(constraint.param)

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
