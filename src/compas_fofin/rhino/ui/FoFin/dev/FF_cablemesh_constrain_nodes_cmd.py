from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

import compas_rhino
from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve
from compas_rhino.geometry import RhinoSurface

from compas_ui.ui import UI
from compas_fd.constraints import Constraint


__commandname__ = "FF_cablemesh_constrain_nodes"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]
    mesh = cablemesh.mesh

    vertices = ui.controller.mesh_select_vertices(cablemesh)
    if not vertices:
        return

    guid = compas_rhino.select_curve(message="Select constraint (Curve/Surface)")
    if not guid:
        return

    obj = compas_rhino.find_object(guid)
    if not obj:
        return

    if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:

        if obj.Geometry.IsLinear():
            line = RhinoLine.from_guid(guid).to_compas()
            constraint = Constraint(line)

        elif obj.Geometry.IsCircle():
            raise NotImplementedError

        elif obj.Geometry.IsEllipse():
            raise NotImplementedError

        elif obj.Geometry.IsArc():
            raise NotImplementedError

        elif obj.Geometry.IsPolyline():
            raise NotImplementedError

        elif isinstance(obj.Geometry, Rhino.Geometry.NurbsCurve):
            curve = RhinoCurve.from_guid(guid).to_compas()
            constraint = Constraint(curve)

        else:
            raise NotImplementedError

    elif obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:

        guid = compas_rhino.select_surface(message="Select surface constraint")
        if not guid:
            return

        surface = RhinoSurface.from_guid(guid).to_compas()
        constraint = Constraint(surface)

    else:
        raise NotImplementedError

    constraint._rhino_guid = str(guid)

    for vertex in vertices:
        constraint.location = mesh.vertex_attributes(vertex, "xyz")
        constraint.project()
        mesh.vertex_attributes(vertex, "xyz", constraint.location)
        mesh.vertex_attribute(vertex, "constraint", constraint)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
