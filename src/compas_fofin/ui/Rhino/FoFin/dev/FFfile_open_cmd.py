from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_fofin.app import App
from compas_fofin.rhino import select_filepath_open
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFfile_open"


HERE = compas_rhino.get_document_dirname()


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    session = App().session

    filepath = select_filepath_open(session.directory, session.extension)
    if filepath:
        session.filepath = filepath
        session.load(filepath)

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
