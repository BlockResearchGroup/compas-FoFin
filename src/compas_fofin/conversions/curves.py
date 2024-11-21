from typing import Union

import Rhino  # type: ignore

import compas.geometry
from compas.geometry import NurbsCurve
from compas_rhino.conversions import circle_to_compas
from compas_rhino.conversions import curve_to_compas_line


def curveobject_to_compas(
    obj: Rhino.DocObjects.CurveObject,
) -> Union[
    compas.geometry.Line,
    compas.geometry.Circle,
    compas.geometry.NurbsCurve,
]:
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
        geometry = NurbsCurve.from_native(obj.Geometry)

    else:
        raise NotImplementedError

    return geometry
