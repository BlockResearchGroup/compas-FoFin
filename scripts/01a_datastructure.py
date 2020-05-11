import compas

from compas.datastructures import Network
from compas_plotters import NetworkPlotter


class Cablenet(Network):

    def __init__(self):
        super(Cablenet, self).__init__()
        self.default_node_attributes.update({
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


cablenet = Cablenet.from_obj(compas.get('lines.obj'))

corners = list(cablenet.nodes_where({'degree': 1}))
cablenet.nodes_attribute('is_anchor', True, keys=corners)

plotter = NetworkPlotter(cablenet, figsize=(8, 5))

plotter.draw_nodes(facecolor={key: '#ff0000' for key in corners})
plotter.draw_edges()
plotter.show()
