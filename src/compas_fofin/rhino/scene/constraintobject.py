import scriptcontext as sc  # type: ignore

import compas.geometry  # noqa: F401
import compas_rhino.conversions
import compas_rhino.objects
from compas_fofin.scene import ConstraintObject
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.scene import RhinoSceneObject


class RhinoConstraintObject(RhinoSceneObject, ConstraintObject):
    """Scene object for drawing constraints in Rhino."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = curve_to_rhino(self.constraint.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddCurve(geometry, attr)]
        return self.guids

    def update_constraint_geometry(self):
        robj = compas_rhino.objects.find_object(self.guids[0])
        curve = compas_rhino.conversions.curveobject_to_compas(robj)
        self.constraint.geometry = curve
        return curve
