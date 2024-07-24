#! python3
import pathlib

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.scene import Scene
from compas_fofin.datastructures import CableMesh
from compas_session.session import Session

__commandname__ = "FF_cablemesh_from_box"


def RunCommand(is_interactive):

    session = Session(root=pathlib.Path(__file__).parent, name="FoFin")

    # =============================================================================
    # Get stuff from session
    # =============================================================================

    scene: Scene = session.setdefault("scene", factory=Scene, filepath="scene.json")
    scene.clear()

    # =============================================================================
    # Make a cablemesh from a box
    # =============================================================================

    guid = compas_rhino.objects.select_object("Select a box")
    if not guid:
        return

    k = rs.GetInteger(message="Resolution", minimum=1, maximum=6, number=2)
    if not k:
        return

    obj = compas_rhino.objects.find_object(guid)
    box = compas_rhino.conversions.extrusion_to_compas_box(obj.Geometry)  # use brep_to_compas_box instead

    mesh = CableMesh.from_shape(box)
    mesh = mesh.subdivided(scheme="quad", k=k)
    mesh.name = "CableMesh"

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.HideObject(guid)

    scene.add(mesh, name=mesh.name)
    scene.draw()

    # =============================================================================
    # Save session
    # =============================================================================

    # session.record()
    # session.save()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
