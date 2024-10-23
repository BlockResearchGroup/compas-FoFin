# import pathlib
# from typing import Union

from compas_session.namedsession import NamedSession

from .settings import Settings


class FoFinSession(NamedSession):
    settings = Settings()

    def __new__(cls, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        return super().__new__(cls, name="FormFinder")

    def __init__(self, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        super().__init__(name="FormFinder", **kwargs)

    def clear(self, clear_scene=True, clear_context=True):
        scene = self.scene()
        for sceneobject in scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()
        scene.clear(clear_scene=clear_scene, clear_context=clear_context)

    def clear_conduits(self):
        scene = self.scene()
        for sceneobject in scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()
