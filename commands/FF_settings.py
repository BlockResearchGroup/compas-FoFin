#! python3
# venv: brg-csd
# r: compas_fofin>=0.15.2

import rhinoscriptsyntax as rs  # type: ignore
from pydantic import BaseModel

from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_rui.forms import NamedValuesForm


def update_settings(model, title):
    names = []
    values = []
    for name, info in model.model_fields.items():
        if issubclass(info.annotation, BaseModel):
            continue
        names.append(name)
        values.append(getattr(model, name))
    form = NamedValuesForm(names, values, title=title)
    if form.show():
        for name, value in form.attributes.items():
            setattr(model, name, value)


# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = FoFinSession()
    session.clear_conduits()

    options = ["Solver", "Drawing", "Display"]

    while True:
        option = rs.GetString(message="Settings Section", strings=options)
        if not option:
            break

        if option == "Solver":
            update_settings(session.settings.solver, title="Solver")

        elif option == "Drawing":
            update_settings(session.settings.drawing, title="Drawing")

        elif option == "Display":
            update_settings(session.settings.display, title="Display")

    # =============================================================================
    # Update scene
    # =============================================================================

    meshobj: RhinoCableMeshObject = session.scene.find_by_name(name="CableMesh")
    if not meshobj:
        return

    meshobj.clear()

    if meshobj.mesh.is_solved:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_forces_conduit(tmax=session.settings.display.tmax)
        meshobj.display_reactions_conduit(scale=session.settings.drawing.scale_reactions)

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit(thickness=session.settings.drawing.edge_thickness)

    meshobj.display_mesh_conduit()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
