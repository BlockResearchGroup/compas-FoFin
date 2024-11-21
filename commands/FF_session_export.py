#! python3
# venv: brg-csd
# r: compas_dr>=0.3, compas_fd>=0.5.2, compas_session>=0.4.5

import rhinoscriptsyntax as rs  # type: ignore

import compas
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_rui.forms import FileForm


def RunCommand():
    session = FoFinSession()

    meshobj: RhinoCableMeshObject = session.scene.find_by_name(name="CableMesh")

    options = ["Scene", "CableMesh"]
    option = rs.GetString(message="Export", strings=options)
    if not option:
        return

    if option == "Scene":
        filepath = FileForm.save(session.basedir, "FormFinder-scene.json")
        if not filepath:
            return

        compas.json_dump(session.scene, filepath)

    elif option == "CableMesh":
        filepath = FileForm.save(session.basedir, "FormFinder-cablemesh.json")
        if not filepath:
            return

        compas.json_dump(meshobj.mesh, filepath)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
