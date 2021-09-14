from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import traceback

import Eto.Drawing as drawing
import Eto.Forms as forms
import Rhino.UI
import compas_fofin
import compas
import Rhino

from functools import wraps


__all__ = ["FF_error"]


def FF_error(title="Error", showLocalTraceback=True):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if showLocalTraceback:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    text = traceback.format_exception(exc_type, exc_value, exc_tb)
                    text = "".join(text)
                else:
                    text = str(error)
                ErrorForm(text, title=title)
        return wrapper
    return outer


ISSUE_TEMPLATE = """---
name: Bug report
about: Create a report to help us improve

---
<!-- The link below shows a list of known-issues and how to fix them -->
<!-- https://blockresearchgroup.gitbook.io/FF/documentation/known-issues -->
<!-- If the error you encounter is not in the list, please describe it as following -->
<!-- We thank you on the feedback -->

**Describe the bug**
```bash
%s
```

**To Reproduce**
Steps to reproduce the behavior:
1. Please provide an input 3dm file
2. Describe the command that causes the error
3. A screenshot of error behavior

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots or video record to help explain your problem.

**Desktop (please complete the following information):**
 - OS: %s
 - Rhino version %s
 - FormFinder version %s

**Additional context**
Add any other context about the problem here.
"""


class ErrorForm(forms.Dialog):

    def __init__(self, error="Unknown", title="Error", width=800, height=400):
        self.Title = title
        self.Padding = drawing.Padding(0)
        self.Resizable = False

        # tab_items = forms.StackLayoutItem(self.TabControl, True)
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch

        self.m_textarea = forms.TextArea()
        self.m_textarea.Size = drawing.Size(400, 400)
        self.m_textarea.Text = error
        self.m_textarea.ReadOnly = True
        layout.Items.Add(self.m_textarea)

        sub_layout = forms.DynamicLayout()
        sub_layout.Spacing = drawing.Size(5, 0)
        sub_layout.AddRow(None, self.report, self.cancel)
        layout.Items.Add(forms.StackLayoutItem(sub_layout))

        self.Content = layout
        self.Padding = drawing.Padding(12)
        self.Resizable = True
        # self.ClientSize = drawing.Size(width, height)

        self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    @property
    def cancel(self):
        self.AbortButton = forms.Button(Text='Close')
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_cancel(self, sender, event):
        self.Close()

    @property
    def report(self):
        self.AbortButton = forms.Button(Text='Report Issue')
        self.AbortButton.Click += self.on_report
        return self.AbortButton

    def on_report(self, sender, event):
        import webbrowser
        title = self.m_textarea.Text.split("\n")[-1] or self.m_textarea.Text.split("\n")[-2]

        _os = "UNKNOWN"
        if compas.WINDOWS:
            _os = "Windows"
        if compas.OSX:
            _os = "OSX"

        body = ISSUE_TEMPLATE % (self.m_textarea.Text, _os, Rhino.RhinoApp.Version, compas_fofin.__version__)
        url = "https://github.com/BlockResearchGroup/FormFinder/issues/new?title=%s&body=%s" % (title, body)
        url = url.replace("\n", "%0A")
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    # error = ErrorForm("TEST")

    @FF_error()
    def break_func():
        raise RuntimeError("some error message")

    break_func()
