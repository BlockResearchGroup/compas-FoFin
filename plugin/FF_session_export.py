#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import rhinoscriptsyntax as rs  # type: ignore

import compas
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_rui.forms import FileForm


def RunCommand(is_interactive):
    session = FoFinSession()

    scene = session.scene()
    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")

    options = ["Scene", "CableMesh"]
    option = rs.GetString(message="Export", strings=options)
    if not option:
        return

    if option == "Scene":
        filepath = FileForm.save(session.basedir, "FormFinder-scene.json")
        if not filepath:
            return

        compas.json_dump(scene, filepath)

    elif option == "CableMesh":
        filepath = FileForm.save(session.basedir, "FormFinder-cablemesh.json")
        if not filepath:
            return

        compas.json_dump(meshobj.mesh, filepath)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
