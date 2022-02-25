from compas_ui.app import App
from compas_cloud import Proxy

SETTINGS = {

    "FF": {
    },

    "Solvers": {
    }
}


class App(App):

    def __init__(self):
        # avoid circular import
        from compas_fofin.rhino import FF_error
        from compas_fofin.scene import Scene

        errorHandler = FF_error(title="Server side Error", showLocalTraceback=False)
        proxy = Proxy(errorHandler=errorHandler, port=9009)
        scene = Scene(SETTINGS)

        super(App, self).__init__(scene=scene, proxy=proxy)

    def load(self, filepath):
        self.session.load(filepath)
        self.update_scene()

    def update_scene(self):
        self.scene.clear()
        if 'settings' in self.session.data:
            self.scene.settings = self.session.data['settings']
        if 'cablemesh' in self.session.data:
            self.scene.add(self.session.data['cablemesh'], name="cablemesh")
        self.scene.update()

    def record_scene(self):
        cablemesh = self.scene.get('cablemesh')[0]
        if cablemesh:
            self.session.data['cablemesh'] = cablemesh.datastructure
        self.session.data['settings'] = self.scene.settings

    def record(self):
        self.record_scene()
        self.session.record()

    def undo(self):
        self.session.undo()
        self.update_scene()

    def redo(self):
        self.session.redo()
        self.update_scene()
