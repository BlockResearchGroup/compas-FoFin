from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System
import Rhino

import compas_rhino

from compas_rhino.geometry import RhinoLine
from compas_rhino.geometry import RhinoCurve

# from compas_rhino.geometry import RhinoSurface

from compas_ui.ui import UI


__commandname__ = "FF_cablemesh_update_constraints"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    result = ui.scene.get(name="CableMesh")
    if not result:
        raise Exception("There is no cablemesh in the scene.")

    cablemesh = result[0]
    mesh = cablemesh.mesh

    for vertex in mesh.vertices_where(is_anchor=True):
        point = mesh.vertex_attributes(vertex, "xyz")
        constraint = mesh.vertex_attribute(vertex, "constraint")

        if not constraint:
            continue

        if not constraint._rhino_guid:
            continue

        result, guid = System.Guid.TryParse(constraint._rhino_guid)

        if not result:
            continue

        obj = compas_rhino.find_object(guid)
        if not obj:
            continue

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:

            if obj.Geometry.IsLinear():
                line = RhinoLine.from_guid(guid).to_compas()
                constraint.geometry = line

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
                constraint.geometry = curve

            else:
                raise NotImplementedError

        elif obj.ObjectType == Rhino.DocObjects.ObjectType.Surface:
            raise NotImplementedError

        constraint.location = point
        constraint.project()
        mesh.vertex_attributes(vertex, "xyz", constraint.location)

    compas_rhino.rs.UnselectAllObjects()
    cablemesh.is_valid = False
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
