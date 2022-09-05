from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from compas_fofin.objects import CableMeshObject


__commandname__ = "FF_cablemesh_solve_dr_numpy"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    cablemesh = ui.scene.active_object

    if not isinstance(cablemesh, CableMeshObject):
        raise Exception("The active object is not a CableMesh.")

    dr = ui.proxy.function("compas.numerical.dr_numpy")

    # cablemesh.update_constraints()

    # k_i = cablemesh.mesh.key_index()
    # vertices = cablemesh.mesh.vertices_attributes("xyz")
    # edges = list(cablemesh.mesh.edges_where(_is_edge=True))
    # fixed = [k_i[vertex] for vertex in cablemesh.mesh.vertices_where(is_anchor=True)]
    # loads = cablemesh.mesh.vertices_attributes(["px", "py", "pz"])
    # qpre = cablemesh.mesh.edges_attribute("q", keys=edges)
    # # fpre, lpre, linit, E, radius
    # kmax = 100

    # ij = [(k_i[u], k_i[v]) for u, v in edges]

    # X, Q, F, L, R = dr(
    #     vertices=vertices,
    #     edges=ij,
    #     fixed=fixed,
    #     loads=loads,
    #     qpre=qpre,
    #     kmax=kmax,
    # )

    # for vertex in cablemesh.mesh.vertices():
    #     index = k_i[vertex]
    #     x = X[index]
    #     r = R[index]
    #     cablemesh.mesh.vertex_attributes(vertex, "xyz", x)
    #     cablemesh.mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"], r)

    # for edge, q, f, l in zip(edges, Q, F, L):
    #     cablemesh.mesh.edge_attribute(edge, "_q", q)
    #     cablemesh.mesh.edge_attribute(edge, "_f", f)
    #     cablemesh.mesh.edge_attribute(edge, "_l", l)

    cablemesh.is_valid = True

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
