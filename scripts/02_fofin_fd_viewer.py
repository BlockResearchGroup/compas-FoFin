import random
import compas

from compas.datastructures import Network
from compas.numerical import fd_numpy
from compas_viewers.objectviewer import ObjectViewer


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


# ==============================================================================
# FoFin
# ==============================================================================

cablenet = Cablenet.from_obj(compas.get('lines.obj'))

corners = list(cablenet.nodes_where({'degree': 1}))
cablenet.nodes_attribute('is_anchor', True, keys=corners)

for key, attr in cablenet.edges(True):
    attr['q'] = random.random()

nodes = cablenet.nodes_attributes('xyz')
edges = list(cablenet.edges())
fixed = list(cablenet.nodes_where({'is_anchor': True}))
loads = cablenet.nodes_attributes(['px', 'py', 'pz'])
q = cablenet.edges_attribute('q')

xyz, q, f, l, r = fd_numpy(nodes, edges, fixed, q, loads)

for key, attr in cablenet.nodes(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]

# ==============================================================================
# Visualisation
# ==============================================================================

anchors = list(cablenet.nodes_where({'is_anchor': True}))
cablenet.nodes_attribute('color', (255, 0, 0), keys=anchors)

viewer = ObjectViewer()
viewer.add(cablenet)
viewer.update()
viewer.show()
