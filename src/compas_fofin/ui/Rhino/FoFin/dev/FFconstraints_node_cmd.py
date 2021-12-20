from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_fd.constraints import Constraint

import compas_rhino
from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
from compas_rhino.geometry import RhinoSurface
from compas_rhino.utilities import select_line
from compas_rhino.utilities import select_curve
from compas_rhino.utilities import select_surface

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error

import FFsolve_fd_cmd


__commandname__ = "FFconstraints_node"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    keys = cablemesh.select_vertices()
    if keys:

        ctype_options = ["Line", "Curve", "Surface"]
        ctype = compas_rhino.rs.GetString("Select node constraints:", strings=ctype_options)

        if not ctype or ctype is None:
            scene.update()
            return
        ctype = ctype.lower()

        if ctype == "line":
            guid = select_line(message="Select line constraint")
            geometry = RhinoLine.from_guid(guid).to_compas()

        elif ctype == "curve":
            guid = select_curve(message="Select curve constraint")
            geometry = RhinoCurve.from_guid(guid).to_compas()

        elif ctype == "surface":
            guid = select_surface(message="Select surface constraint")
            geometry = RhinoSurface.from_guid(guid).to_compas()

        constraint = Constraint(geometry)
        constraint.guid = guid
        for key in keys:
            constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
            constraint.project()
            cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
            cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        cablemesh.settings['_is.valid'] = False
        compas_rhino.rs.UnselectAllObjects()
        if scene.settings['FF']['autoupdate']:
            FFsolve_fd_cmd.RunCommand(True)
        else:
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
