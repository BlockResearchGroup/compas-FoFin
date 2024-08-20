import os

import Eto.Forms
import Rhino.UI
import System


class FileForm(Eto.Forms.Dialog[bool]):
    @staticmethod
    def open(dirname=None):
        dirname = dirname or os.path.expanduser("~")
        dialog = Eto.Forms.OpenFileDialog()
        if dirname:
            dialog.Directory = System.Uri(dirname)
        dialog.MultiSelect = False
        result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
        if result != Eto.Forms.DialogResult.Ok:
            return
        return dialog.FileName

    @staticmethod
    def save(dirname=None, basename=None):
        dirname = dirname or os.path.expanduser("~")
        dialog = Eto.Forms.SaveFileDialog()
        if dirname:
            dialog.Directory = System.Uri(dirname)
        dialog.FileName = basename
        result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
        if result != Eto.Forms.DialogResult.Ok:
            return
        return dialog.FileName


class FolderForm(Eto.Forms.Dialog[bool]):
    @staticmethod
    def select(dirname=None):
        dirname = dirname or os.path.expanduser("~")
        dialog = Eto.Forms.SelectFolderDialog()
        dialog.Directory = dirname
        result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
        if result != Eto.Forms.DialogResult.Ok:
            return
        return dialog.Directory
