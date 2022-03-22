from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.app import App


__commandname__ = "FF_cablemesh_modify_edges"


@App.error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]

    edges = app.select_mesh_edges(cablemesh)
    if not edges:
        return

    scale = app.get_real("Scale factor?", minval=1e-3, maxval=1e+3, default=1.0)

    if scale:
        Q = cablemesh.mesh.edges_attribute('q', keys=edges)
        Q = [q * scale for q in Q]
        for edge, q in zip(edges, Q):
            cablemesh.mesh.edge_attribute(edge, 'q', q)
        cablemesh.is_valid = False
        app.scene.update()
        app.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
