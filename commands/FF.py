#! python3
# venv: brg-csd

import pathlib

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
import System  # type: ignore

pluginfile = Rhino.PlugIns.PlugIn.PathFromId(System.Guid("5df3b821-822e-49e0-b24e-aebbe671c3d1"))
shared = pathlib.Path(str(pluginfile)).parent / "shared"


class SplashForm(Eto.Forms.Dialog[bool]):
    def __init__(self, title, url, width=800, height=400):
        super().__init__()

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(width, height)
        self.WindowStyle = Eto.Forms.WindowStyle.NONE  # type: ignore

        webview = Eto.Forms.WebView()
        webview.Size = Eto.Drawing.Size(width, height)
        webview.Url = System.Uri(url)
        webview.BrowserContextMenuEnabled = False
        webview.DocumentLoading += self.action

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical()
        layout.AddRow(webview)
        layout.EndVertical()
        self.Content = layout

    def action(self, sender, e):
        if e.Uri.Scheme == "action" and e.Uri.Host == "close":
            self.Close()

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


def RunCommand():
    form = SplashForm(title="FormFinder", url=str(shared / "index.html"))
    form.show()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
