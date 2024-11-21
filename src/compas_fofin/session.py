import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.settings import FoFinSettings
from compas_session.session import Session


class FoFinSession(Session):
    settings: FoFinSettings

    def __new__(cls, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        return super().__new__(cls, name="FormFinder")

    def __init__(self, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        super().__init__(name="FormFinder", settings=FoFinSettings(), **kwargs)

    def clear(self, clear_scene=True, clear_context=True):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()
        self.scene.clear(clear_scene=clear_scene, clear_context=clear_context)

    def clear_conduits(self):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()

    def confirm(self, message):
        result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
        return result == 6

    def warn(self, message):
        return rs.MessageBox(message, title="Warning")
