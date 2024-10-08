#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

import compas_rhino.objects
from compas_fofin.scene import RhinoConstraintObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="FormFinder")
    scene = session.scene()
    scene.redraw()

    for obj in scene.objects:
        if isinstance(obj, RhinoConstraintObject):
            robj = compas_rhino.objects.find_object(obj.guids[0])
            robj.UserDictionary["constraint.guid"] = str(obj.constraint.guid)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
