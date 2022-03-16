from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms.error import error
from compas_ui.app import App


__commandname__ = 'FF_undo'


@error()
def RunCommand(is_interactive):

    app = App()
    app.undo()


if __name__ == '__main__':
    RunCommand(True)