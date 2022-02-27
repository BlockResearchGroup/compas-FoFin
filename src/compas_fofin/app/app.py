from compas_ui.app import App
from compas_fofin.rhino import FF_error
from compas_fofin.scene import Scene
from compas_cloud import Proxy


class App(App):

    SETTINGS = {}

    # local init-ing should be avoided in case of apps
    # the plugin mechanism shoould provide plenty of options to modify the behaviour
    # perhaps we can use the Flask App API (or similar) as inspiration
    def __init__(self):
        # this is very opaque behaviour
        # it is not clear what this handler is supposed to be used for
        # perhaps compas_cloud should provide this as a pluggable
        # furthermore, since we add this decorator also to the RunCommand functions
        # can we not just let the cloud error bubble up to there and let it be handled by those handlers?
        # the undo/redo/error decorators should also be defined in compas_ui rather than here
        # and as pluggables
        errorHandler = FF_error(title="Server side Error", showLocalTraceback=False)
        # starting a proxy only requires som basic settings
        # and can be handled by the base app
        # the settings could be in a mandatory external config.json file
        proxy = Proxy(errorHandler=errorHandler, port=9009)
        # a scene should also not be local
        scene = Scene(App.SETTINGS)
        # also not sure if this is the correct way to about this
        super(App, self).__init__(scene=scene, proxy=proxy)

    def load(self, filepath):
        self.session.load(filepath)
        self.update_scene()

    def record(self):
        # i don't think it makes sense that the data has to be rerived from the scene
        # to be able to record it
        # the data should be in the session in the first place
        # the scene only manages the representation of that data
        # commands and operations should always just modify the data in the session
        # the ui simply reflects those changes
        # we could add watchpoints to the session data and scene settings to keep track of objects
        # only when they are changed the scene has to be updated
        cablemesh = self.scene.get('cablemesh')[0]
        if cablemesh:
            self.session.data['cablemesh'] = cablemesh.datastructure
        # about the scene settings this is less clear of course
        # settings and scene settings are not necessarily the same thing, btw
        self.session.data['settings'] = self.scene.settings
        self.session.record()

    def undo(self):
        self.session.undo()
        self.update_scene()

    def redo(self):
        self.session.redo()
        self.update_scene()

    def update_scene(self):
        self.scene.clear()
        if 'settings' in self.session.data:
            self.scene.settings = self.session.data['settings']
        if 'cablemesh' in self.session.data:
            self.scene.add(self.session.data['cablemesh'], name="cablemesh")
        self.scene.update()
