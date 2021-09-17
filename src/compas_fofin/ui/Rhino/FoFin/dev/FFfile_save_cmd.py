from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

from compas.utilities import DataEncoder

import compas_rhino
from compas_fofin.rhino import get_system
from compas_fofin.rhino import get_scene
from compas_fofin.rhino import select_filepath_save
from compas_fofin.rhino import FF_error
from compas_fofin.rhino import save_session


__commandname__ = "FFfile_save"


HERE = compas_rhino.get_document_dirname()


@FF_error()
def RunCommand(is_interactive):

    system = get_system()
    if not system:
        return

    scene = get_scene()
    if not scene:
        return

    dirname = system['session.dirname']
    filename = system['session.filename']
    extension = system['session.extension']

    filepath = select_filepath_save(dirname, extension)
    if not filepath:
        return
    dirname, basename = os.path.split(filepath)
    filename, _ = os.path.splitext(basename)

    filepath = os.path.join(dirname, filename + '.' + extension)

    # this should be templated somewhere
    # perhaps there should be a Session class/object/singleton

    session = save_session()

    with open(filepath, 'w+') as f:
        json.dump(session, f, cls=DataEncoder)


# ==============================================================================sc
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
