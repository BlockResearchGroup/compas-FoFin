#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_rhino.objects
from compas.colors import Color
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.scene import RhinoConstraintObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")

    scene = session.scene()

    if session.redo():
        scene.clear()
        scene = session.scene()
        scene.draw()

        meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

        if meshobj:
            for sceneobject in scene.objects:
                if isinstance(sceneobject, RhinoConstraintObject):
                    scene.clear_context(sceneobject.guids)
                    scene.remove(sceneobject)

            mesh: CableMesh = meshobj.mesh

            for guid in mesh.constraints:
                constraint = mesh.constraints[guid]
                sceneobject = scene.add(constraint, color=Color.cyan())
                sceneobject.draw()

                robj = compas_rhino.objects.find_object(sceneobject.guids[0])
                robj.UserDictionary["constraint.guid"] = str(guid)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
