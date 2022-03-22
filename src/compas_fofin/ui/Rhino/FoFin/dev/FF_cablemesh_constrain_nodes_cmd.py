from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Frame

import compas_rhino
from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
from compas_rhino.geometry import RhinoSurface

from compas_ui.app import App
from compas_fd.constraints import Constraint


__commandname__ = "FF_cablemesh_constrain_nodes"


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    vertices = app.select_mesh_vertices(cablemesh)
    if not vertices:
        return

    ctypes = ["Direction", "Line", "Plane", "Curve", "Surface"]
    ctype = app.get_string("Node constraint type?", options=ctypes)
    if not ctype:
        return

    if ctype == "Direction":
        cdirs = ["X", "Y", "Z", "XY", "YZ", "ZX"]
        cdir = app.get_string("Constraint direction?", options=cdirs)
        if not cdir:
            return

        if cdir in ["X", "Y", "Z"]:

            if cdir == "X":
                vector = Vector.Xaxis()
            elif cdir == "Y":
                vector = Vector.Yaxis()
            elif cdir == "Z":
                vector = Vector.Zaxis()

            constraint = Constraint(vector)
            mesh.vertices_attribute('constraint', constraint, keys=vertices)

        elif cdir in ["XY", "YZ", "ZX"]:

            if cdir == "XY":
                vectors = Vector.Xaxis(), Vector.Yaxis()
            elif cdir == "YZ":
                vectors = Vector.Yaxis(), Vector.Zaxis()
            elif cdir == "ZX":
                vectors = Vector.Zaxis(), Vector.Xaxis()

            for vertex in vertices:
                origin = mesh.vertex_attributes(vertex, 'xyz')
                frame = Frame(origin, *vectors)
                constraint = Constraint(frame)
                mesh.vertices_attribute('constraint', constraint, keys=vertices)

    elif ctype == "Line":
        guid = compas_rhino.select_line(message="Select line constraint")
        if not guid:
            return

        line = RhinoLine.from_guid(guid).to_compas()
        constraint = Constraint(line)
        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, 'xyz')
            constraint.project()
            mesh.vertex_attributes(vertex, 'xyz', constraint.location)
            mesh.vertex_attribute(vertex, 'constraint', constraint)

    elif ctype == "Plane":
        guid = compas_rhino.select_line(message="Select plane constraint")
        if not guid:
            return

        line = RhinoLine.from_guid(guid).to_compas()
        plane = Plane(line.start, line.vector)
        constraint = Constraint(plane)
        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, 'xyz')
            constraint.project()
            mesh.vertex_attributes(vertex, 'xyz', constraint.location)
            mesh.vertex_attribute(vertex, 'constraint', constraint)

    elif ctype == "Curve":
        guid = compas_rhino.select_curve(message="Select curve constraint")
        if not guid:
            return

        curve = RhinoCurve.from_guid(guid).to_compas()
        constraint = Constraint(curve)
        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, 'xyz')
            constraint.project()
            mesh.vertex_attributes(vertex, 'xyz', constraint.location)
            mesh.vertex_attribute(vertex, 'constraint', constraint)

    elif ctype == "Surface":
        guid = compas_rhino.select_surface(message="Select surface constraint")
        if not guid:
            return

        surface = RhinoSurface.from_guid(guid).to_compas()
        constraint = Constraint(surface)
        for vertex in vertices:
            constraint.location = mesh.vertex_attributes(vertex, 'xyz')
            constraint.project()
            mesh.vertex_attributes(vertex, 'xyz', constraint.location)
            mesh.vertex_attribute(vertex, 'constraint', constraint)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    app.scene.update()
    app.record()


if __name__ == "__main__":
    RunCommand(True)
