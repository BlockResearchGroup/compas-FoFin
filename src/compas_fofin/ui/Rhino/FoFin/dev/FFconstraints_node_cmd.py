from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import add_vectors, scale_vector

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

        options = ["Direction", "Line", "Plane"]
        option = compas_rhino.rs.GetString("Select node constraints:", strings=options)

        if not option:
            return

        if option == "Direction":
            options2 = ["x", "y", "z", "XY", "YZ", "ZX"]
            option2 = compas_rhino.rs.GetString("Select direction constraint:", strings=options2)

            if not option2:
                return

            key = keys[0]  # placeholder
            scale = 1  # placeholder

            if option2 == "x" or option2 == "y" or option2 == "z":

                if option2 == "x":
                    vector = Vector.Xaxis()
                elif option2 == "y":
                    vector = Vector.Yaxis()
                elif option2 == "z":
                    vector = Vector.Zaxis()

                start = cablemesh.datastructure.vertex_coordinates(key)
                end = add_vectors(start, scale_vector(vector, scale))
                constraint = Line(start, end)

            elif option2 == "XY" or option2 == "YZ" or option2 == "ZX":

                if option2 == "XY":
                    vector = Vector.Zaxis()
                elif option2 == "YZ":
                    vector = Vector.Xaxis()
                elif option2 == "ZX":
                    vector = Vector.Yaxis()

                origin = cablemesh.datastructure.vertex_coordinates(key)
                constraint = Plane(origin, vector)

        elif option == "Line":
            guid = select_line(message="Select line constraint")
            obj = compas_rhino.find_object(guid)
            constraint = Line(obj.Geometry.PointAtStart, obj.Geometry.PointAtEnd)  # to be reaplced by constraint object

        elif option == "Plane":
            raise NotImplementedError

        # store constraint as attribute to the cablemesh, to_data to be removed for latest compas dev
        cablemesh.datastructure.vertices_attribute('constraint', constraint.to_data(), keys=keys)

        # visualise constraint
        print(constraint)

        cablemesh.settings['_is.valid'] = False
        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
