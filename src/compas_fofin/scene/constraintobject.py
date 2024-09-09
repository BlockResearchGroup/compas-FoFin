import scriptcontext as sc  # type: ignore

import compas.geometry  # noqa: F401  # noqa: F401
import compas_rhino.conversions
import compas_rhino.objects
from compas_fd.constraints import Constraint  # noqa: F401
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.scene import RhinoSceneObject


class RhinoConstraintObject(RhinoSceneObject):
    def __init__(self, **kwargs):  # type: (...) -> None
        super().__init__(**kwargs)

        # del kwargs["item"]
        # self.add(item=self.constraint.geometry, **kwargs)

    @property
    def constraint(self):
        # type: () -> Constraint
        return self.item

    @constraint.setter
    def constraint(self, constraint):
        self.item = constraint
        self._transformation = None

    @property
    def transformation(self):
        # type: () -> compas.geometry.Transformation | None
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
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
