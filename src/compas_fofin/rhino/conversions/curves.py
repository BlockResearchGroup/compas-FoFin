import Rhino

from compas_rhino.geometry import RhinoNurbsCurve
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import circle_to_compas

# from compas_rhino.geometry import RhinoCircle
# from compas_rhino.geometry import RhinoEllipse


def curveobject_to_compas(obj):
    if obj.Geometry.IsLinear():
        geometry = curve_to_compas_line(obj.Geometry)

    elif obj.Geometry.IsCircle():
        result, circle = obj.Geometry.TryGetCircle()
        geometry = circle_to_compas(circle)

    elif obj.Geometry.IsEllipse():
        raise NotImplementedError

    elif obj.Geometry.IsArc():
        raise NotImplementedError

    elif obj.Geometry.IsPolyline():
        raise NotImplementedError

    elif isinstance(obj.Geometry, Rhino.Geometry.NurbsCurve):
        geometry = RhinoNurbsCurve.from_rhino(obj.Geometry)

    else:
        raise NotImplementedError

    return geometry
