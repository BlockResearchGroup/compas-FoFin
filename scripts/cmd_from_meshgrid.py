import compas_rhino
from compas_fofin.app import App
from compas_fofin.datastructures import CableMesh

# this should raise an error in case there is no instance yet
# app = ui.instance()
# alternatively, the syntax for this is ui = UI()
# and the syntax used by the init command is app = ui.init(proxy=..., scene=...)

def RunCommand():
    ui = UI()

    dx = compas_rhino.rs.GetReal("Dimension in X direction:", 10.0, 1.0, 100.0)
    if not dx or dx is None:
        ui.scene.update()
        return

    nx = compas_rhino.rs.GetInteger("Number of faces in X direction:", 10, 2, 100)
    if not nx or nx is None:
        ui.scene.update()
        return

    dy = compas_rhino.rs.GetReal("Dimension in the Y direction:", dx, 1.0, 100.0)
    if not dy or dy is None:
        ui.scene.update()
        return

    ny = compas_rhino.rs.GetInteger("Number of faces in Y direction:", nx, 2, 100)
    if not ny or ny is None:
        ui.scene.update()
        return

    mesh = CableMesh.from_meshgrid(dx, nx, dy, ny)

    # basically, like in blender, create a new data block
    ui.session.data[mesh.guid] = mesh  # ui.session.add(mesh)

    # clearing the scene is a special case
    ui.scene.clear()

    # add the data block to the scene by converting it into an object
    # the object should maintain a reference to the data block
    ui.scene.add(mesh, name='cablemesh')

    ui.scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
