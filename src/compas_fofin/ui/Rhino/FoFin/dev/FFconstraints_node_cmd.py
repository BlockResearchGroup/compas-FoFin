from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import add_vectors, scale_vector

from compas_fd.constraints import Constraint

import compas_rhino
from compas_rhino.utilities import select_line

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_error


__commandname__ = "FFconstraints_node"

scale = 1  # placeholder


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

        options = ["Direction", "Line", "Plane", "Curve", "Surface"]
        option = compas_rhino.rs.GetString("Select node constraints:", strings=options)

        constraints = []

        if not option:
            return

        if option == "Direction":
            options2 = ["x", "y", "z", "xy", "yz", "zx"]
            option2 = compas_rhino.rs.GetString("Select direction constraint:", strings=options2)

            if not option2:
                return

            if option2 in ["x", "y", "z"]:

                if option2 == "x":
                    vector = Vector.Xaxis()
                elif option2 == "y":
                    vector = Vector.Yaxis()
                elif option2 == "z":
                    vector = Vector.Zaxis()

                for key in keys:
                    start = cablemesh.datastructure.vertex_coordinates(key)
                    end = add_vectors(start, scale_vector(vector, scale))
                    line = Line(start, end)
                    constraint = Constraint(line)
                    constraints.append(constraint.to_data())

            elif option2 in ["xy", "yz", "zx"]:

                if option2 == "xy":
                    vector = Vector.Zaxis()
                elif option2 == "yz":
                    vector = Vector.Xaxis()
                elif option2 == "zx":
                    vector = Vector.Yaxis()

                for key in keys:
                    origin = cablemesh.datastructure.vertex_coordinates(key)
                    plane = Plane(origin, vector)
                    constraint = Constraint(plane)
                    constraints.append(constraint.to_data())

        elif option == "Line":
            guid = select_line(message="Select line constraint")
            obj = compas_rhino.find_object(guid)
            line = Line(obj.Geometry.PointAtStart, obj.Geometry.PointAtEnd)
            constraint = Constraint(line)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                constraints.append(constraint.to_data())

        elif option == "Plane":
            guid = select_line(message="Select plane constraint")
            obj = compas_rhino.find_object(guid)
            line = Line(obj.Geometry.PointAtStart, obj.Geometry.PointAtEnd)
            plane = Plane(line.start, line.vector)
            constraint = Constraint(plane)
            for key in keys:
                constraint.location = cablemesh.datastructure.vertex_attributes(key, 'xyz')
                constraint.project()
                cablemesh.datastructure.vertex_attributes(key, 'xyz', constraint.location)
                constraints.append(constraint.to_data())

        elif option == "Curve":
            raise NotImplementedError

        elif option == "Surface":
            raise NotImplementedError

        cablemesh.datastructure.vertices_attribute('constraint', constraints, keys=keys)

        # visualise constraint
        print(cablemesh.datastructure.data)

        cablemesh.settings['_is.valid'] = False
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
