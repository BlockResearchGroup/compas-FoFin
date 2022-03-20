from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten

from compas_ui.rhino.forms import error
from compas_ui.app import App


__commandname__ = "FF_cablemesh_modify_edges"


@error()
def RunCommand(is_interactive):

    app = App()

    result = app.scene.get(name='CableMesh')
    if not result:
        raise Exception('There is no cablemesh in the scene.')

    cablemesh = result[0]
    mesh = cablemesh.mesh

    options = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]
    mode = app.get_string(message="Selection mode.", options=options)
    if not mode:
        return

    if mode == 'All':
        edges = list(mesh.edges())

    elif mode == 'AllBoundaryEdges':
        edges = list(set(flatten(mesh.edges_on_boundaries())))
        guids = [cablemesh.edge_guid[edge] for edge in edges]
        app.scene.highlight_objects(guids)

    elif mode == 'Continuous':
        temp = cablemesh.select_edges()
        edges = list(set(flatten([mesh.edge_loop(edge) for edge in temp])))
        guids = [cablemesh.edge_guid[edge] for edge in edges]
        app.scene.highlight_objects(guids)

    elif mode == 'Parallel':
        temp = cablemesh.select_edges()
        edges = list(set(flatten([mesh.edge_strip(edge) for edge in temp])))
        guids = [cablemesh.edge_guid[edge] for edge in edges]
        app.scene.highlight_objects(guids)

    elif mode == 'Manual':
        edges = cablemesh.select_edges()

    if edges:
        public = [name for name in mesh.default_edge_attributes.keys() if not name.startswith('_')]
        if cablemesh.modify_edges(edges, names=public):
            cablemesh.is_valid = False
            app.scene.update()
            app.record()

    compas_rhino.rs.UnselectAllObjects()


if __name__ == "__main__":
    RunCommand(True)
