from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import add_vectors

from compas_fd.constraints import Constraint

import compas_rhino
from compas_rhino.utilities import select_line

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
        ctype = compas_rhino.rs.GetString("Select node constraints:", strings=ctype_options)

        if not ctype:
            return

        if ctype == "Direction":
            cdir_options = ["x", "y", "z", "xy", "yz", "zx"]
            cdir = compas_rhino.rs.GetString("Select cdir constraint:", strings=cdir_options).lower()

            if not cdir:
                return

            if cdir in ["x", "y", "z"]:

                if cdir == "x":
                    vector = Vector.Xaxis()
                elif cdir == "y":
                    vector = Vector.Yaxis()
                elif cdir == "z":
                    vector = Vector.Zaxis()

                for key in keys:
                    start = cablemesh.datastructure.vertex_coordinates(key)
                    end = add_vectors(start, vector)
                    line = Line(start, end)
                    constraint = Constraint(line)
                    cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

            elif cdir in ["xy", "yz", "zx"]:

                if cdir == "xy":
                    vector = Vector.Zaxis()
                elif cdir == "yz":
                    vector = Vector.Xaxis()
                elif cdir == "zx":
                    vector = Vector.Yaxis()

                for key in keys:
                    origin = cablemesh.datastructure.vertex_coordinates(key)
                    plane = Plane(origin, vector)
                    constraint = Constraint(plane)
                    cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Line":
            guid = select_line(message="Select line constraint")
            obj = compas_rhino.find_object(guid)
            line = Line(obj.Geometry.PointAtStart, obj.Geometry.PointAtEnd)
            constraint = Constraint(line)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Plane":
            guid = select_line(message="Select plane constraint")
            obj = compas_rhino.find_object(guid)
            line = Line(obj.Geometry.PointAtStart, obj.Geometry.PointAtEnd)
            plane = Plane(line.start, line.vector)
            constraint = Constraint(plane)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                cablemesh.datastructure.vertex_attribute(key, 'constraint', constraint)

        elif ctype == "Curve":
            raise NotImplementedError

        elif ctype == "Surface":
            raise NotImplementedError

        cablemesh.settings['_is.valid'] = False
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
