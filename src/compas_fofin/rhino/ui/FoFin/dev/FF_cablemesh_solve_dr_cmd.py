from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.numerical import dr
from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_solve_dr"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    mesh = cablemesh.mesh

    k_i = mesh.key_index()
    vertices = mesh.vertices_attributes("xyz")
    edges = list(mesh.edges_where({"_is_edge": True}))
    ij = [(k_i[u], k_i[v]) for u, v in edges]
    fixed = [k_i[vertex] for vertex in mesh.vertices_where(is_anchor=True)]
    loads = mesh.vertices_attributes(["px", "py", "pz"])
    qpre = mesh.edges_attribute("q", keys=mesh.edges_where({"_is_edge": True}))
    # fpre
    # lpre
    # linit
    # E
    # radius
    kmax = 100

    X, Q, F, L, R = dr(
        vertices=vertices,
        edges=ij,
        fixed=fixed,
        loads=loads,
        qpre=qpre,
        kmax=kmax,
    )

    for vertex in mesh.vertices():
        index = k_i[vertex]
        x = X[index]
        r = R[index]
        mesh.vertex_attributes(vertex, "xyz", x)
        mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"], r)

    for edge, q, f, l in zip(edges, Q, F, L):
        mesh.edge_attribute(edge, "_q", q)
        mesh.edge_attribute(edge, "_f", f)
        mesh.edge_attribute(edge, "_l", l)

    cablemesh.is_valid = True

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
