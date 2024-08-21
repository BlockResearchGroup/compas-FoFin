from compas.colors import Color
from compas.scene import MeshObject
from compas.scene.descriptors.color import ColorAttribute


class CableMeshObject(MeshObject):

    anchorcolor = ColorAttribute(default=Color.red())
    constraintcolor = ColorAttribute(default=Color.cyan())
    residualcolor = ColorAttribute(default=Color.cyan())
    reactioncolor = ColorAttribute(default=Color.green())
    loadcolor = ColorAttribute(default=Color.green().darkened(50))
    selfweightcolor = ColorAttribute(default=Color.black())
    compressioncolor = ColorAttribute(default=Color.blue())
    tensioncolor = ColorAttribute(default=Color.red())

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.show_anchors = True
        self.show_free = False
        self.show_forces = False
        self.show_residuals = False
        self.show_reactions = True

        self.scale_loads = 1
        self.scale_forces = 1
        self.scale_residuals = 50
        self.scale_selfweight = 1

        self.is_valid = False

    @property
    def settings(self):
        settings = super().settings
        settings["show_forces"] = self.show_forces
        settings["show_residuals"] = self.show_residuals
        settings["show_reactions"] = self.show_reactions
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
