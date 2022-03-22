import compas_rhino
from compas_fofin.app import App
from compas_fofin.datastructures import CableMesh

# this should raise an error in case there is no instance yet
# app = App.instance()
# alternatively, the syntax for this is app = App()
# and the syntax used by the init command is app = App.init(proxy=..., scene=...)

def RunCommand():
    app = App()

    dx = compas_rhino.rs.GetReal("Dimension in X direction:", 10.0, 1.0, 100.0)
    if not dx or dx is None:
        app.scene.update()
        return

    nx = compas_rhino.rs.GetInteger("Number of faces in X direction:", 10, 2, 100)
    if not nx or nx is None:
        app.scene.update()
        return

    dy = compas_rhino.rs.GetReal("Dimension in the Y direction:", dx, 1.0, 100.0)
    if not dy or dy is None:
        app.scene.update()
        return

    ny = compas_rhino.rs.GetInteger("Number of faces in Y direction:", nx, 2, 100)
    if not ny or ny is None:
        app.scene.update()
        return

    mesh = CableMesh.from_meshgrid(dx, nx, dy, ny)

    # basically, like in blender, create a new data block
    app.session.data[mesh.guid] = mesh  # app.session.add(mesh)

    # clearing the scene is a special case
    app.scene.clear()

    # add the data block to the scene by converting it into an object
    # the object should maintain a reference to the data block
    app.scene.add(mesh, name='cablemesh')

    app.scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
