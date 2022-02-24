from compas_ui.session import Session


class Session(Session):

    def load(self, filepath):
        super(Session, self).load(filepath)
        self.load_to_scene()

    def load_to_scene(self):
        self.scene.clear()
        if 'settings' in self.data:
            self.scene.settings = self.data['settings']
        if 'cablemesh' in self.data:
            self.scene.add(self.data['cablemesh'], name="cablemesh")
        self.scene.update()

    def save_from_scene(self):
        cablemesh = self.scene.get('cablemesh')[0]
        if cablemesh:
            self['cablemesh'] = cablemesh.datastructure
        self['settings'] = self.scene.settings

    def record(self):
        self.save_from_scene()
        super(Session, self).record()

    def undo(self):
        super(Session, self).undo()
        self.load_to_scene()

    def redo(self):
        super(Session, self).redo()
        self.load_to_scene()
