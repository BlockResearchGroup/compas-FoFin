import Eto.Drawing
import Eto.Forms
import Rhino
import Rhino.UI


class InfoForm(Eto.Forms.Dialog[bool]):
    def __init__(self, text, title="Info", width=800, height=500):
        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)
        textarea = Eto.Forms.TextArea()
        textarea.Text = text
        textarea.ReadOnly = True
        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(12, 12, 12, 0), Eto.Drawing.Size(0, 0), True, True)
        layout.AddRow(textarea)
        layout.EndVertical()
        layout.BeginVertical(Eto.Drawing.Padding(12, 12, 12, 18), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(None, self.ok)
        layout.EndVertical()
        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    def on_ok(self, sender, event):
        self.Close(True)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
