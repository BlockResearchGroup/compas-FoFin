from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import pairwise
from compas_rhino.conversions import RhinoCylinder
from compas_ui.ui import UI
from compas_fofin.datastructures import CableMesh


__commandname__ = "FF_cablemesh_from_cylinder"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    guid = compas_rhino.select_object("Select a cylinder")
    if not guid:
        return

    U = ui.get_integer(
        "Number of faces along perimeter",
        minval=4,
        maxval=64,
        default=16,
    )
    if not U:
        return

    V = ui.get_integer(
        "Number of faces along height",
        minval=2,
        maxval=32,
        default=4,
    )
    if not V:
        return

    cylinder = RhinoCylinder.from_guid(guid).to_compas()
    mesh = CableMesh.from_shape(cylinder, u=U)
    mesh.name = "CableMesh"

    # move this to somewhere else
    # ---------------------------------------
    # ---------------------------------------

    # remove top/bottom
    mesh.delete_vertex((U * 2) + 1)
    mesh.delete_vertex(U * 2)

    # split for subdivison along length
    start = None
    for edge in mesh.edges():
        if not mesh.is_edge_on_boundary(*edge):
            start = edge
            break

    strip = mesh.edge_strip(start)
    if strip[0] == strip[-1]:
        strip[:] = strip[:-1]

    splits = []
    for u, v in strip:
        start = mesh.vertex_point(u)
        vector = mesh.edge_vector((u, v))
        temp = [u]
        w = u
        for i in range(V - 1):
            t = (i + 1) * 1 / V
            point = start + vector * t
            w = mesh.split_edge(w, v, t=0.5)
            mesh.vertex_attributes(w, "xyz", point)
            temp.append(w)
        temp.append(v)
        splits.append(temp)

    faces = list(mesh.faces())
    for face in faces:
        mesh.delete_face(face)

    for right, left in pairwise(splits + splits[0:1]):
        for (a, b), (aa, bb) in zip(pairwise(right), pairwise(left)):
            mesh.add_face([a, b, bb, aa])

    # ---------------------------------------
    # ---------------------------------------

    compas_rhino.rs.HideObject(guid)
    ui.scene.add(mesh, name=mesh.name)
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
