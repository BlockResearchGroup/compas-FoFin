from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import __plugin__ as PLUGIN

import os
import compas_rhino

from compas_ui.rhino.forms.browser import BrowserForm
from compas_ui.rhino.forms.error import error
from compas_ui.app import App


__commandname__ = "FF_init"

HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME
SPLASH = os.path.join(os.path.dirname(__file__), 'splash', 'index.html')


@error()
def RunCommand(is_interactive):

    # check __plugin__ for required env
    # if this is not the same as active env in compas_bootstrapper
    # notify the user

    App._instances = {}

    browser = BrowserForm(title=PLUGIN.title, url=SPLASH)
    browser.show()

    app = App(name=PLUGIN.title, settings=PLUGIN.settings)
    app.scene.clear()


if __name__ == '__main__':
    RunCommand(True)