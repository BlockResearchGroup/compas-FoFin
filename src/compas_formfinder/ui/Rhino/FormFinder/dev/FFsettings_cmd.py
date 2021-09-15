from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_formfinder.rhino import get_scene
from compas_formfinder.rhino import SettingsForm
from compas_formfinder.rhino import FF_error


__commandname__ = "FFsettings"


@FF_error()
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    SettingsForm.from_scene(scene, object_types=["CableMeshObject"], global_settings=["FF", "Solvers"])

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
