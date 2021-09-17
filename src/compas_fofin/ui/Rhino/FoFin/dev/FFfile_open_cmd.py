from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

from compas.utilities import DataDecoder

import compas_rhino
from compas_fofin.rhino import get_system
from compas_fofin.rhino import get_scene
from compas_fofin.rhino import select_filepath_open
from compas_fofin.rhino.helpers import load_session
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFfile_open"


HERE = compas_rhino.get_document_dirname()


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    system = get_system()
    if not system:
        return

    scene = get_scene()
    if not scene:
        return

    filepath = select_filepath_open(system['session.dirname'], system['session.extension'])
    if not filepath:
        return

    dirname, basename = os.path.split(filepath)
    filename, extension = os.path.splitext(basename)

    system['session.dirname'] = dirname
    system['session.filename'] = filename

    with open(filepath, "r") as f:
        session = json.load(f, cls=DataDecoder)

    load_session(session)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
