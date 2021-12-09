from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoCylinder
from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_from_cylinder"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_object(message='Select cylinder.')

    if not guid:
        return

    # u = compas_rhino.rs.GetInteger("Number of faces along perimeter:", 32, 3, 100)
    sub_perimeter = compas_rhino.rs.GetInteger("Number of levels of subdivision along perimeter:", 3, 2, 20)
    sub_height = compas_rhino.rs.GetInteger("Number of levels of subdivision along height:", 3, 0, 20)
    u = 2**(sub_perimeter)

    cylinder = RhinoCylinder.from_guid(guid).to_compas()
    cablemesh = CableMesh.from_shape(cylinder, u=u)

    # remove top/bottom
    cablemesh.delete_vertex((u*2)+1)
    cablemesh.delete_vertex(u*2)

    # split for subdivison along length
    start = None
    for edge in cablemesh.edges():
        if not cablemesh.is_edge_on_boundary(*edge):
            start = edge
            break

    for i in range(sub_height):
        if i == 0:
            vertices = cablemesh.split_strip(start)
        else:
            parallel = cablemesh.edge_strip((vertices[0], vertices[1]))
            for edge in parallel[:-1]:
                cablemesh.split_strip(cablemesh.halfedge_after(*edge))

    compas_rhino.rs.HideObject(guid)

    scene.clear()
    scene.add(cablemesh, name='cablemesh')
    scene.update()

    print("CableMesh object successfully created. Input cylinder has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
