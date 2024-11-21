import scriptcontext as sc  # type: ignore

import compas.geometry
import compas_rhino.conversions
import compas_rhino.objects
from compas_fd.constraints import Constraint
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.scene import RhinoSceneObject


class RhinoConstraintObject(RhinoSceneObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def constraint(self) -> Constraint:
        return self.item

    @constraint.setter
    def constraint(self, constraint: Constraint) -> None:
        self.item = constraint
        self._transformation = None

    @property
    def transformation(self) -> compas.geometry.Transformation:
        return self._transformation

    @transformation.setter
    def transformation(self, transformation: compas.geometry.Transformation) -> None:
        self._transformation = transformation

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

    def clear(self):
        """Clear all components of the constraint.

        Returns
        -------
        None

        """
        raise NotImplementedError
