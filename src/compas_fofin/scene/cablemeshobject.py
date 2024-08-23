from compas.colors import Color
from compas.scene import MeshObject
from compas.scene.descriptors.color import ColorAttribute


class CableMeshObject(MeshObject):
    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    constraintcolor = ColorAttribute(default=Color.cyan())
    residualcolor = ColorAttribute(default=Color.cyan())
    reactioncolor = ColorAttribute(default=Color.green())
    loadcolor = ColorAttribute(default=Color.green().darkened(50))
    selfweightcolor = ColorAttribute(default=Color.white())
    compressioncolor = ColorAttribute(default=Color.blue())
    tensioncolor = ColorAttribute(default=Color.red())

    def __init__(
        self,
        show_anchors=True,
        show_free=False,
        show_forces=False,
        show_residuals=False,
        show_reactions=False,
        show_loads=False,
        show_selfweight=False,
        scale_loads=1,
        scale_forces=1,
        scale_residuals=1,
        scale_selfweight=1,
        tol_vectors=1e-3,
        tol_pipes=1e-3,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.show_anchors = show_anchors
        self.show_free = show_free
        self.show_forces = show_forces
        self.show_residuals = show_residuals
        self.show_reactions = show_reactions
        self.show_loads = show_loads
        self.show_selfweight = show_selfweight

        self.scale_loads = scale_loads
        self.scale_forces = scale_forces
        self.scale_residuals = scale_residuals
        self.scale_selfweight = scale_selfweight

        self.tol_vectors = tol_vectors
        self.tol_pipes = tol_pipes

        self.is_valid = False

    @property
    def settings(self):
        settings = super().settings

        settings["show_anchors"] = self.show_anchors
        settings["show_free"] = self.show_free
        settings["show_forces"] = self.show_forces
        settings["show_residuals"] = self.show_residuals
        settings["show_reactions"] = self.show_reactions
        settings["show_loads"] = self.show_loads
        settings["show_selfweight"] = self.show_selfweight

        settings["scale_loads"] = self.scale_loads
        settings["scale_forces"] = self.scale_forces
        settings["scale_residuals"] = self.scale_residuals
        settings["scale_selfweight"] = self.scale_selfweight

        settings["tol_vectors"] = self.tol_vectors
        settings["tol_pipes"] = self.tol_pipes

        settings["freecolor"] = self.freecolor
        settings["anchorcolor"] = self.anchorcolor
        settings["constraintcolor"] = self.constraintcolor
        settings["residualcolor"] = self.residualcolor
        settings["reactioncolor"] = self.reactioncolor
        settings["loadcolor"] = self.loadcolor
        settings["selfweightcolor"] = self.selfweightcolor
        settings["compressioncolor"] = self.compressioncolor
        settings["tensioncolor"] = self.tensioncolor

        return settings

    def select_vertices(self):
        raise NotImplementedError

    def select_edges(self):
        raise NotImplementedError

    def select_faces(self):
        raise NotImplementedError

    def draw_forces(self):
        raise NotImplementedError

    def draw_residuals(self):
        raise NotImplementedError

    def draw_reactions(self):
        raise NotImplementedError

    def draw_loads(self):
        raise NotImplementedError

    def draw_selfweight(self):
        raise NotImplementedError
