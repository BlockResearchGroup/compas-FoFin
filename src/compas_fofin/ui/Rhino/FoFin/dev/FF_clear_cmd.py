from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.app import App


__commandname__ = 'FF_clear'


@App.error()
def RunCommand(is_interactive):

    compas_rhino.clear()

    app = App()
    app.clear()
    app.record()

    compas_rhino.redraw()


if __name__ == '__main__':
    RunCommand(True)
