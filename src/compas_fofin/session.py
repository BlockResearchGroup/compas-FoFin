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
                sceneobject.clear_conduits()  # type: ignore
        self.scene.clear(clear_scene=clear_scene, clear_context=clear_context)

    def clear_conduits(self):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()  # type: ignore

    def confirm(self, message):
        result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
        return result == 6

    def warn(self, message):
        return rs.MessageBox(message, title="Warning")

    def find_cablemesh(self, warn=True):
        from compas_fofin.datastructures import CableMesh
        from compas_fofin.scene import RhinoCableMeshObject

        cablemesh: RhinoCableMeshObject = self.scene.find_by_itemtype(CableMesh)  # type: ignore
        if cablemesh:
            return cablemesh
        if warn:
            rs.MessageBox("There is no CableMesh.", title="Warning")
