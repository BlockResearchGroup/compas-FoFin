
# the first part stays exactly the same 
# except the removal of the import of the Rhino Artist 
# and adding the import of the viewer
import compas
from compas.geometry import Point, Vector, Line
from compas_view2.app import App
from compas_view2.objects import Collection

FILE = '/Users/aldinger/Desktop/CableMesh.json'
cablemesh = compas.json_load(FILE)

reactions = []
for key, attr in cablemesh.vertices(data=True):
    if attr['is_anchor']:
        start = Point(*cablemesh.vertex_coordinates(key))
        reaction = Vector(attr['_rx'], attr['_ry'], attr['_rz'])
        line = Line(start, start-reaction)
        reactions.append(line)

normals = []       
for key in cablemesh.vertices():
    start = Point(*cablemesh.vertex_coordinates(key))
    normal = Vector(*cablemesh.vertex_normal(key))
    line = Line(start, start+normal*0.1)
    normals.append(line)

# the visualistion part is modified to the COMPAS viewer 
# so that working with COMPAS is independent of Rhino
viewer = App()

collection = Collection(reactions)
viewer.add(collection)

collection = Collection(normals)
viewer.add(collection)

viewer.add(cablemesh)

viewer.show()
