from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_ui.ui import UI


__commandname__ = 'FF_clear'


@UI.error()
def RunCommand(is_interactive):

    compas_rhino.clear()

    ui = UI()
    ui.clear()
    # ui.record()

    compas_rhino.redraw()


if __name__ == '__main__':
    RunCommand(True)
