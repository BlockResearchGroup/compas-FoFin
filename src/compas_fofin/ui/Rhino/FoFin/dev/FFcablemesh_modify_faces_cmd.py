from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.utilities import flatten

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_modify_faces"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["All", "AllBoundaryFaces", "Strip", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options)

    if not option:
        return

    if option == "All":
        keys = keys = list(cablemesh.datastructure.faces())

    elif option == "AllBoundaryFaces":
        keys = cablemesh.datastructure.faces_on_boundary()

    elif option == "Strip":
        edge = cablemesh.select_edges()[0]
        edge_strip = cablemesh.datastructure.edge_strip(edge)
        keys = [cablemesh.datastructure.edge_faces(u, v) for (u, v) in edge_strip]
        keys = [i for i in list(set(flatten(keys))) if i is not None]

    elif option == "Manual":
        keys = cablemesh.select_faces()

    if keys:
        public = [name for name in cablemesh.datastructure.default_face_attributes.keys() if not name.startswith('_')]
        if cablemesh.update_faces_attributes(keys, names=public):
            cablemesh.settings['_is.valid'] = False
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
