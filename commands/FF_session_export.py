#! python3
# venv: brg-csd
# r: compas_fofin>=0.15.2

import pathlib

# import rhinoscriptsyntax as rs  # type: ignore
import compas
from compas.datastructures import Mesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_rui.forms import FileForm


def RunCommand():
    session = FoFinSession()

    meshobj: RhinoCableMeshObject = session.find_cablemesh()
    if not meshobj:
        return

    # options = ["Scene", "CableMesh"]
    # option = rs.GetString(message="Export", strings=options)
    # if not option:
    #     return

    # if option == "Scene":
    #     filepath = FileForm.save(session.basedir, "FormFinder-Scene.json")
    #     if not filepath:
    #         return

    #     compas.json_dump(session.scene, filepath)

    # elif option == "CableMesh":

    mesh: Mesh = meshobj.mesh.copy()
    for face in list(mesh.faces_where(_is_loaded=False)):
        mesh.delete_face(face)

    basedir = session.basedir or pathlib.Path().home()
    basename = "FormFinder-Cablemesh.json"
    filepath = FileForm.save(str(basedir), basename)
    if not filepath:
        return

    compas.json_dump(mesh, filepath)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
