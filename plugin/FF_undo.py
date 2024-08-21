#! python3
import compas_rhino.objects
from compas.colors import Color
from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.rhino.scene import RhinoConstraintObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    scene: Scene = session.setdefault("scene", factory=Scene)

    if session.undo():
        scene.clear()
        scene: Scene = session.setdefault("scene", factory=Scene)
        scene.draw()

        # recreate links

        meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

        if meshobj:
            for obj in scene.objects:
                if isinstance(obj, RhinoConstraintObject):
                    scene.remove(obj)

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
