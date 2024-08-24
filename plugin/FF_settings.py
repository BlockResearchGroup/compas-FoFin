#! python3
import ast

import rhinoscriptsyntax as rs  # type: ignore

from compas_fofin.datastructures import CableMesh
from compas_fofin.rhino.scene import RhinoCableMeshObject
from compas_fofin.session import Session


def RunCommand(is_interactive):

    session = Session(name="FormFinder")
    scene = session.scene()

    option = rs.GetString(message="Update Settings", strings=["SessionConfig", "CableMeshObject", "CableMesh"])
    if not option:
        return

    if option == "SessionConfig":
        names = sorted(list(session.CONFIG.keys()))
        values = [session.CONFIG[name] for name in names]

        values = rs.PropertyListBox(names, values, message="Update Config", title="FormFinder")

        if values:
            for name, value in zip(names, values):
                try:
                    session.CONFIG[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    session.CONFIG[name] = value

    elif option == "CableMeshObject":
        meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")

        if meshobj:
            names = []
            values = []
            for name in sorted(list(meshobj.settings.keys())):
                value = getattr(meshobj, name)
                if isinstance(value, (bool, int, float, str)):
                    names.append(name)
                    values.append(value)

            values = rs.PropertyListBox(names, values, message="Update CableMesh Object Settings", title="FormFinder")

            if values:
                for name, value in zip(names, values):
                    try:
                        setattr(meshobj, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        setattr(meshobj, name, value)

    elif option == "CableMesh":
        meshobj: RhinoCableMeshObject = scene.get_node_by_name(name="CableMesh")
        mesh: CableMesh = meshobj.mesh

        if mesh:
            names = []
            values = []
            for name in sorted(list(mesh.attributes.keys())):
                value = mesh.attributes[name]
                if isinstance(value, (bool, int, float, str)):
                    names.append(name)
                    values.append(value)

            values = rs.PropertyListBox(names, values, message="Update CableMesh Attributes", title="FormFinder")

            if values:
                for name, value in zip(names, values):
                    try:
                        mesh.attributes[name] = ast.literal_eval(value)
                    except (ValueError, TypeError):
                        mesh.attributes[name] = value

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
