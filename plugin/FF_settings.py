#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5.2, compas_rui>=0.3, compas_session>=0.3

import dataclasses

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.scene import RhinoCableMeshObject
from compas_fofin.session import FoFinSession
from compas_rui.forms import NamedValuesForm


def RunCommand(is_interactive):
    session = FoFinSession()
    session.clear_conduits()

    options = ["Solver", "Drawing", "Display"]
    option = rs.GetString(message="Settings Section", strings=options)
    if not option:
        return

    if option == "Solver":
        fields = dataclasses.fields(session.settings.solver.__class__)
        names = [field.name for field in fields]
        values = [getattr(session.settings.solver, name) for name in names]
        form = NamedValuesForm(names, values, title="Solver Settings")
        if form.show():
            for name, value in form.attributes.items():
                setattr(session.settings.solver, name, value)

    elif option == "Drawing":
        fields = dataclasses.fields(session.settings.drawing.__class__)
        names = [field.name for field in fields]
        values = [getattr(session.settings.drawing, name) for name in names]
        form = NamedValuesForm(names, values, title="Drawing Settings")
        if form.show():
            for name, value in form.attributes.items():
                setattr(session.settings.drawing, name, value)

    elif option == "Display":
        fields = dataclasses.fields(session.settings.display.__class__)
        names = [field.name for field in fields]
        values = [getattr(session.settings.display, name) for name in names]
        form = NamedValuesForm(names, values, title="Display Settings")
        if form.show():
            for name, value in form.attributes.items():
                setattr(session.settings.display, name, value)

    # =============================================================================
    # Update scene
    # =============================================================================

    scene = session.scene()

    meshobj: RhinoCableMeshObject = scene.find_by_name(name="CableMesh")
    if not meshobj:
        return

    meshobj.clear()

    if meshobj.mesh.is_solved:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_forces_conduit(tmax=session.settings.display.tmax)
        meshobj.display_reactions_conduit()

    else:
        meshobj.show_vertices = list(meshobj.mesh.vertices_where(is_support=True))
        meshobj.show_edges = False
        meshobj.show_faces = False
        meshobj.draw()
        meshobj.display_edges_conduit()

    meshobj.display_mesh_conduit()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
