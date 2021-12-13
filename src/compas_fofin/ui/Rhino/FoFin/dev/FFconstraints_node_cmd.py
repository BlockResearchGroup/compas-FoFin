from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Frame

from compas_fd.constraints import Constraint

import compas_rhino
from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
# from compas_rhino.geometry import RhinoSurface
from compas_rhino.utilities import select_line
from compas_rhino.utilities.objects import select_curve
# from compas_rhino.utilities.objects import select_surface

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error


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

        ctype_options = ["Direction", "Line", "Plane", "Curve", "Surface"]
        ctype = compas_rhino.rs.GetString("Select node constraints:", strings=ctype_options).lower()

        if not ctype or ctype is None:
            return

        if ctype == "Eirection":
            cdir_options = ["X", "Y", "Z", "XY", "YZ", "ZX"]
            cdir = compas_rhino.rs.GetString("Select direction constraint:", strings=cdir_options).lower()

            if not cdir or cdir is None:
                return

            if cdir in ["X", "Y", "Z"]:

                if cdir == "X":
                    vector = Vector.Xaxis()
                elif cdir == "Y":
                    vector = Vector.Yaxis()
                elif cdir == "Z":
                    vector = Vector.Zaxis()

                constraint = Constraint(vector)
                cablemesh.datastructure.vertices_attribute('constraint', constraint, keys=keys)

            elif cdir in ["XY", "YZ", "ZX"]:

                if cdir == "XY":
                    vectors = Vector.Xaxis(), Vector.Yaxis()
                elif cdir == "YZ":
                    vectors = Vector.Yaxis(), Vector.Zaxis()
                elif cdir == "ZX":
                    vectors = Vector.Zaxis(), Vector.Xaxis()

                for key in keys:
                    origin = cablemesh.datastructure.vertex_coordinates(key)
                    frame = Frame(origin, *vectors)
                    constraint = Constraint(frame)
                    cablemesh.datastructure.vertices_attribute('constraint', constraint, keys=keys)

        elif ctype == "Line":
            guid = select_line(message="Select line constraint")
            line = RhinoLine.from_guid(guid).to_compas()
            constraint = Constraint(line)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Plane":
            guid = select_line(message="Select plane constraint")
            line = RhinoLine.from_guid(guid).to_compas()
            plane = Plane(line.start, line.vector)
            constraint = Constraint(plane)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Curve":
            guid = select_curve(message="Select curve constraint")
            curve = RhinoCurve.from_guid(guid).to_compas()
            constraint = Constraint(curve)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Surface":
            # guid = select_surface(message="Select surface constraint")
            # curve = RhinoSurface.from_guid(guid).to_compas()
            # constraint = Constraint(curve)
            # for key in keys:
            #     constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
            #     constraint.project()
            #     cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
            #     cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)
            raise NotImplementedError

        cablemesh.settings['_is.valid'] = False
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
