from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI


__commandname__ = 'FF_clear'


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene.update()


if __name__ == '__main__':
    RunCommand(True)
