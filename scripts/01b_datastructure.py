import compas

from compas.datastructures import Mesh
from compas_plotters import MeshPlotter


class Cablenet(Mesh):

    def __init__(self):
        super(Cablenet, self).__init__()
        self.default_vertex_attributes.update({
            'is_anchor': False,
            'is_fixed': False,
            'px': 0.0,
            'py': 0.0,
            'pz': 0.0,
            'rx': 0.0,
            'ry': 0.0,
            'rz': 0.0
        })
        self.default_edge_attributes.update({
            'q': 1.0,
            'f': None,
            'l': None,
            'l0': None,
            'E': None,
            'radius': None
        })


cablenet = Cablenet.from_obj(compas.get('faces.obj'))

corners = list(cablenet.vertices_where({'vertex_degree': 2}))
cablenet.vertices_attribute('is_anchor', True, keys=corners)

plotter = MeshPlotter(cablenet, figsize=(8, 5))
plotter.draw_vertices(facecolor={key: '#ff0000' for key in corners})
plotter.draw_edges()
plotter.show()
