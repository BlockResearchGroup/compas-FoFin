#! python3
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.scene import Scene
from compas_fofin.rhino.conversions import box_to_cablemesh
from compas_fofin.rhino.conversions import cylinder_to_cablemesh
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")

    # =============================================================================
    # Get stuff from session
    # =============================================================================

    scene: Scene = session.setdefault("scene", factory=Scene)
    scene.clear()

    # =============================================================================
    # Make a CableMesh "Pattern"
    # =============================================================================

    option = rs.GetString(message="CableMesh From", strings=["RhinoBox", "RhinoCylinder", "MeshGrid"])

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
        cylinder = compas_rhino.conversions.brep_to_compas_cylinder(obj.Geometry)
        mesh = cylinder_to_cablemesh(cylinder, U, V, name="CableMesh")

        rs.HideObject(guid)

    elif option == "RhinoMesh":
        pass

    elif option == "MeshGrid":
        pass

    else:
        return

    # =============================================================================
    # Update scene
    # =============================================================================

    scene.add(mesh, name=mesh.name)
    scene.draw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.CONFIG["autosave"]:
        session.record(eventname="Make Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
