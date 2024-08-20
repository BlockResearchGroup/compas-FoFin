import Eto.Forms
import Rhino.UI
import System

import compas_fofin


class AboutForm:
    def __init__(self):
        self.dialog = Eto.Forms.AboutDialog()
        self.dialog.Copyright = compas_fofin.__copyright__
        self.dialog.Designers = System.Array[System.String](compas_fofin.designers)
        self.dialog.Developers = System.Array[System.String](compas_fofin.developers)
        self.dialog.Documenters = System.Array[System.String](compas_fofin.documenters)
        self.dialog.License = compas_fofin.__license__
        self.dialog.ProgramDescription = compas_fofin.description
        self.dialog.ProgramName = compas_fofin.title
        self.dialog.Title = compas_fofin.title
        self.dialog.Version = compas_fofin.__version__
        self.dialog.Website = System.Uri(compas_fofin.website)

    def show(self):
        self.dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
