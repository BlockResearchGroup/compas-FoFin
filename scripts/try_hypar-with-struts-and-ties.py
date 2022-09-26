from compas.data import Data
from compas.geometry import Point, Line, Polyline
from compas.geometry import Cylinder
from compas.geometry import discrete_coons_patch
from compas.datastructures import Graph
from compas.utilities import geometric_key
from compas.colors import Color

from compas_fofin.datastructures import CableMesh
from compas_fd.fd import fd_numpy

from compas_view2.app import App


class Assembly(Data):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = {}
        self.splines = {}
        self.patches = {}
        self.graph = Graph()
        self.graph.update_default_node_attributes(
            is_external=False, px=0.0, py=0.0, pz=0.0, rx=0.0, ry=0.0, rz=0.0, t=0.0
        )
        self.graph.update_default_edge_attributes(
            vertex=None,
            q=1.0,
            f=0.0,
            l=0.0,
        )

    def node_point(self, node):
        if node in self.points:
            return Point(self.points[node])

    def edge_line(self, edge):
        a = self.points.get(edge[0])
        b = self.points.get(edge[1])
        if a and b:
            return Line(a, b)

    def add_strut(self, u, v, **kwargs):
        pass

    def add_tie(self, u, v, **kwargs):
        pass


# =============================================================================
# Init the assembly
# =============================================================================

assembly = Assembly()

# =============================================================================
# Add (interaction) nodes
# =============================================================================

A0 = Point(0, 0, 0)

B0 = Point(0, 10, 7)
B1 = Point(0, 10, 0)
B2 = Point(-3, 10, 0)
B3 = Point(0, 13, 0)

C0 = Point(10, 10, 0)

D0 = Point(10, 0, 7)
D1 = Point(10, 0, 0)
D2 = Point(13, 0, 0)
D3 = Point(10, -3, 0)

a0 = assembly.graph.add_node(is_external=True)
assembly.points[a0] = A0

b0 = assembly.graph.add_node(is_external=True)
assembly.points[b0] = B0

b1 = assembly.graph.add_node(is_external=True)
assembly.points[b1] = B1

b2 = assembly.graph.add_node(is_external=True)
assembly.points[b2] = B2

b3 = assembly.graph.add_node(is_external=True)
assembly.points[b3] = B3

c0 = assembly.graph.add_node(is_external=True)
assembly.points[c0] = C0

d0 = assembly.graph.add_node(is_external=True)
assembly.points[d0] = D0

d1 = assembly.graph.add_node(is_external=True)
assembly.points[d1] = D1

d2 = assembly.graph.add_node(is_external=True)
assembly.points[d2] = D2

d3 = assembly.graph.add_node(is_external=True)
assembly.points[d3] = D3

# =============================================================================
# Add mesh patch (like a cablemesh)
# =============================================================================

AB = Polyline((A0, B0))
AB = Polyline(AB.divide(10))

BC = Polyline((B0, C0))
BC = Polyline(BC.divide(10))

DC = Polyline((D0, C0))
DC = Polyline(DC.divide(10))

AD = Polyline((A0, D0))
AD = Polyline(AD.divide(10))

vertices, faces = discrete_coons_patch(AB, BC, DC, AD)
mesh = CableMesh.from_vertices_and_faces(vertices, faces)
mesh.update_default_vertex_attributes(interaction=None)

p1 = assembly.graph.add_node()
assembly.patches[p1] = mesh

# link mesh vertices to assembly (interaction) points

gkey_vertex = mesh.gkey_vertex()

a0_gkey = geometric_key(assembly.points[a0])
b0_gkey = geometric_key(assembly.points[b0])
c0_gkey = geometric_key(assembly.points[c0])
d0_gkey = geometric_key(assembly.points[d0])

assembly.graph.add_edge(a0, p1, vertex=gkey_vertex[a0_gkey])
assembly.graph.add_edge(b0, p1, vertex=gkey_vertex[b0_gkey])
assembly.graph.add_edge(c0, p1, vertex=gkey_vertex[c0_gkey])
assembly.graph.add_edge(d0, p1, vertex=gkey_vertex[d0_gkey])

mesh.vertex_attribute(gkey_vertex[a0_gkey], "interaction", a0)
mesh.vertex_attribute(gkey_vertex[b0_gkey], "interaction", b0)
mesh.vertex_attribute(gkey_vertex[c0_gkey], "interaction", c0)
mesh.vertex_attribute(gkey_vertex[d0_gkey], "interaction", d0)

boundary = mesh.edges_on_boundary()
mesh.edges_attribute("q", 5, keys=boundary)

# =============================================================================
# Add struts and ties
# =============================================================================

assembly.graph.add_edge(b0, b1, is_strut=True)
assembly.graph.add_edge(b0, b2)
assembly.graph.add_edge(b0, b3)

assembly.graph.add_edge(d0, d1, is_strut=True)
assembly.graph.add_edge(d0, d2)
assembly.graph.add_edge(d0, d3)

# =============================================================================
# Numerical data
# =============================================================================

index = 0
node_index = {}
xyz = []
fixed = []
edges = []
forcedensities = []

for node in assembly.graph.nodes():
    if node in assembly.points:
        point = assembly.points[node]
        xyz.append(point)
        node_index[node] = index
        index += 1

        if assembly.graph.node_attribute(node, "is_external"):
            fixed.append(node_index[node])

for edge in assembly.graph.edges():
    if edge[0] in assembly.points:
        i = node_index[edge[0]]
        if edge[1] in assembly.points:
            j = node_index[edge[1]]
            edges.append((i, j))
            forcedensities.append(assembly.graph.edge_attribute(edge, "q"))

for node in assembly.patches:
    mesh: CableMesh = assembly.patches[node]
    vertex_index = {}

    for vertex in mesh.vertices():
        interaction = mesh.vertex_attribute(vertex, "interaction")
        if interaction is not None:
            vertex_index[vertex] = node_index[interaction]
        else:
            point = Point(*mesh.vertex_attributes(vertex, "xyz"))
            xyz.append(point)
            vertex_index[vertex] = index
            index += 1

    mesh.attributes["vertex_index"] = vertex_index

    for edge in mesh.edges_where(_is_edge=True):
        i = vertex_index[edge[0]]
        j = vertex_index[edge[1]]
        edges.append((i, j))
        forcedensities.append(mesh.edge_attribute(edge, "q"))

# print(xyz)
# print(edges)
# print(forcedensities)
# print(fixed)

# assert len(edges) == len(forcedensities)

# =============================================================================
# Run FD
# =============================================================================

result = fd_numpy(
    vertices=xyz,
    fixed=fixed,
    edges=edges,
    forcedensities=forcedensities,
    loads=None,
)

vertices = result.vertices

for node in assembly.graph.nodes():
    if node in assembly.points:
        index = node_index[node]
        point = assembly.points[node]
        x, y, z = vertices[index]
        point.x = x
        point.y = y
        point.z = z

for node in assembly.patches:
    mesh: CableMesh = assembly.patches[node]
    for vertex in mesh.vertices():
        index = mesh.attributes["vertex_index"][vertex]
        xyz = vertices[index]
        mesh.vertex_attributes(vertex, "xyz", xyz)

# =============================================================================
# Visualize
# =============================================================================

viewer = App()

for node in assembly.graph.nodes():
    if node in assembly.points:
        if assembly.graph.node_attribute(node, "is_external"):
            pointcolor = (1, 0, 0)
        else:
            pointcolor = (0, 0, 0)
        viewer.add(assembly.points[node], pointsize=20, pointcolor=pointcolor)
    elif node in assembly.patches:
        viewer.add(assembly.patches[node])

for edge in assembly.graph.edges():
    if edge[0] in assembly.patches or edge[1] in assembly.patches:
        continue

    line = assembly.edge_line(edge)
    if assembly.graph.edge_attribute(edge, "is_strut"):
        strut = Cylinder(((line.midpoint, line.direction), 0.050), line.length)
        viewer.add(strut, facecolor=Color.navy())
    else:
        viewer.add(line)

viewer.show()
