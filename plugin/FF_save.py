#! python3
# from compas.scene import Scene
from compas_fofin.rhino.forms.filesystem import FileForm

# from compas_fofin.rhino.scene import RhinoCableMeshObject
# from compas_fofin.rhino.scene import RhinoConstraintObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")
    # scene: Scene = session.setdefault("scene", factory=Scene)

    filepath = FileForm.save(session.basedir, "FormFinder.json")
    if not filepath:
        return

    # meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

    # if meshobj:
    #     for obj in scene.objects:
    #         if isinstance(obj, RhinoConstraintObject):
    #             scene.remove(obj)

    session.save(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
