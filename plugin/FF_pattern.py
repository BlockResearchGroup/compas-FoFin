#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas_fofin.conversions import box_to_cablemesh
from compas_fofin.conversions import cylinder_to_cablemesh
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession


def RunCommand(is_interactive):
    session = FoFinSession()

    # =============================================================================
    # Get stuff from session
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")

    # =============================================================================
    # Confirmation
    # =============================================================================

    if meshobj:
        result = rs.MessageBox(
            "This will remove all current FormFinder data and objects. Do you wish to proceed?",
            buttons=4 | 32 | 256 | 0,
            title="FormFinder",
        )
        if result == 6:
            session.clear()

    # =============================================================================
    # Make a CableMesh "Pattern"
    # =============================================================================

    option = rs.GetString(message="CableMesh From", strings=["RhinoBox", "RhinoCylinder", "RhinoMesh", "RhinoSurface", "MeshGrid"])

    if option == "RhinoBox":
        guid = compas_rhino.objects.select_object("Select a box")
        if not guid:
            return

        k = rs.GetInteger(message="Resolution", minimum=1, maximum=6, number=2)
        if not k:
            return

        obj = compas_rhino.objects.find_object(guid)
        box = compas_rhino.conversions.extrusion_to_compas_box(obj.Geometry)
        mesh = box_to_cablemesh(box, k=k, name="CableMesh")

        rs.HideObject(guid)

    elif option == "RhinoCylinder":
        guid = compas_rhino.objects.select_object("Select a cylinder")
        if not guid:
            return

        U = rs.GetInteger(message="Number of faces along perimeter", number=16, minimum=4, maximum=64)
        if not U:
            return

        V = rs.GetInteger(message="Number of faces along height", number=4, minimum=2, maximum=32)
        if not V:
            return

        obj = compas_rhino.objects.find_object(guid)
        cylinder = compas_rhino.conversions.extrusion_to_compas_cylinder(obj.Geometry)
        mesh = cylinder_to_cablemesh(cylinder, U, V, name="CableMesh")

        rs.HideObject(guid)

    elif option == "RhinoMesh":
        guid = compas_rhino.objects.select_mesh("Select a mesh")
        if not guid:
            return

        obj = compas_rhino.objects.find_object(guid)
        mesh = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=CableMesh)

        rs.HideObject(guid)

    elif option == "RhinoSurface":
        guid = compas_rhino.objects.select_surface("Select a surface")
        if not guid:
            return

        U = rs.GetInteger(message="U faces", number=16, minimum=2, maximum=64)
        if not U:
            return

        V = rs.GetInteger(message="V faces", number=4, minimum=2, maximum=64)
        if not V:
            return

        # ------------------------------------------------

        obj = compas_rhino.objects.find_object(guid)
        brep = obj.Geometry
        surface = brep.Surfaces[0]

        # ------------------------------------------------

        mesh = compas_rhino.conversions.surface_to_compas_mesh(surface, nu=U, nv=V, weld=True, cls=CableMesh)

        rs.HideObject(guid)

    elif option == "MeshGrid":
        DX = rs.GetInteger(message="X Size", number=10)
        if not DX:
            return

        DY = rs.GetInteger(message="Y Size", number=DX)
        if not DY:
            return

        NX = rs.GetInteger(message="Number of faces in X", number=10)
        if not NX:
            return

        NY = rs.GetInteger(message="Number of faces in Y", number=NX)
        if not NY:
            return

        mesh = CableMesh.from_meshgrid(dx=DX, nx=NX, dy=DY, ny=NY)

    else:
        return

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj = scene.add(mesh, name=mesh.name)

    meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
    meshobj.show_edges = True
    meshobj.show_faces = False

    meshobj.draw()
    meshobj.display_mesh_conduit()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Make Pattern")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
