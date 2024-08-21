import compas.geometry  # noqa: F401
from compas.scene import SceneObject
from compas_fd.constraints import Constraint  # noqa: F401


class ConstraintObject(SceneObject):
    def __init__(self, **kwargs):  # type: (...) -> None
        super(ConstraintObject, self).__init__(**kwargs)
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
        """Draw the constraint.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear all components of the constraint.

        Returns
        -------
        None

        """
        raise NotImplementedError
