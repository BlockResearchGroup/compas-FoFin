from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import __plugin__ as PLUGIN

import os
import compas_rhino

from compas_ui.app import App


__commandname__ = "FF_init"

HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME
SPLASH = os.path.join(os.path.dirname(__file__), 'splash', 'index.html')


@App.error()
def RunCommand(is_interactive):

    # check __plugin__ for required env
    # if this is not the same as active env in compas_bootstrapper
    # notify the user

    App.reset()

    app = App(name=PLUGIN.title, settings=PLUGIN.settings)
    app.clear()
    app.splash(url=SPLASH)


if __name__ == '__main__':
    RunCommand(True)
