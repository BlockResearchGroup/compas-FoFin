import scriptcontext as sc  # type: ignore

import compas.geometry  # noqa: F401
from compas_fofin.scene import ConstraintObject
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.scene import RhinoSceneObject


class RhinoConstraintObject(RhinoSceneObject, ConstraintObject):
    """Scene object for drawing constraints in Rhino."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @property
    # def guids(self):
    #     guids = []
    #     for child in self.children:
    #         guids += child.guids
    #     return guids

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

    # def clear_(self):
    #     compas_rhino.clear(guids=self.guids)

    # def draw_(self):
    #     for child in self.children:
    #         child.draw()
    #         robj = compas_rhino.objects.find_object(child.guids[0])
    #         robj.UserDictionary["constraint.guid"] = str(self.constraint.guid)

    #     return self.guids
