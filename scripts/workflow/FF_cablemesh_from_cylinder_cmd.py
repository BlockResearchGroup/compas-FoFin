#! python3
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.itertools import pairwise
from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_session.session import Session

__commandname__ = "FF_cablemesh_from_cylinder"


def RunCommand(is_interactive):

    session = Session()

    # =============================================================================
    # Load stuff from session
    # =============================================================================

    scene: Scene = session.load_data("scene.json")

    # =============================================================================
    # Get params
    # =============================================================================

    guid = compas_rhino.objects.select_object("Select a cylinder")
    if not guid:
        return

    U = rs.GetInteger(
        message="Number of faces along perimeter",
        number=16,
        minimum=4,
        maximum=64,
    )
    if not U:
        return

    V = rs.GetInteger(
        message="Number of faces along height",
        number=4,
        minimum=2,
        maximum=32,
    )
    if not V:
        return

    # =============================================================================
    # Create mesh from cylinder
    # =============================================================================

    obj = compas_rhino.objects.find_object(guid)
    cylinder = compas_rhino.conversions.brep_to_compas_cylinder(obj.Geometry)
    mesh = CableMesh.from_shape(cylinder, u=U)
    mesh.name = "CableMesh"

    # remove top/bottom
    for vertex in list(mesh.vertices_where(vertex_degree=U)):
        mesh.delete_vertex(vertex)

    # split for subdivison along length
    start = None
    for edge in mesh.edges():
        if not mesh.is_edge_on_boundary(*edge):
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
            w = mesh.split_edge(w, v, t=0.5)
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

    # =============================================================================
    # Hide the input object
    # =============================================================================

    rs.HideObject(guid)

    # =============================================================================
    # Save session data
    # =============================================================================

    session.save_data(mesh, "CableMesh.json")

    # =============================================================================
    # Visualize
    # =============================================================================

    scene.add(mesh, name="CableMesh", layer="FormFinder")
    scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
