from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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

    ctypes = ["Line", "Curve", "Surface"]
    ctype = app.get_string("Node constraint type?", options=ctypes)
    if not ctype:
        return

    if ctype == "Line":
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
