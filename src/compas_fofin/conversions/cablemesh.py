from compas.itertools import pairwise
from compas_fofin.datastructures import CableMesh


def box_to_cablemesh(box, k, name=None):
    # type(...) -> CableMesh
    mesh = CableMesh.from_shape(box)  # type: CableMesh
    mesh = mesh.subdivided(scheme="quad", k=k)
    mesh.name = name or "CableMesh"
    return mesh


def cylinder_to_cablemesh(cylinder, U, V, name=None):
    # type(...) -> CableMesh
    mesh = CableMesh.from_shape(cylinder, u=U)  # type: CableMesh
    mesh.name = name or "CableMesh"

    # remove top/bottom
    for vertex in list(mesh.vertices_where(vertex_degree=U)):
        mesh.delete_vertex(vertex)

    # split for subdivison along length
    start = None
    for edge in mesh.edges():
        if not mesh.is_edge_on_boundary(edge):
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
            w = mesh.split_edge((w, v), t=0.5)
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

    mesh.remove_duplicate_vertices()

    return mesh
