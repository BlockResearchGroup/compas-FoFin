from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoMesh
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error
from compas_ui.app import App


__commandname__ = "FFcablemesh_from_mesh"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    cablemesh = RhinoMesh.from_guid(guid).to_compas(cls=CableMesh)

    compas_rhino.rs.HideObject(guid)

    app = App()
    app.scene.clear()
    app.scene.add(cablemesh, name='cablemesh')
    app.scene.update()

    print("CableMesh object successfully created. Input mesh has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
