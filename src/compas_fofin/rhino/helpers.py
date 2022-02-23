from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from ast import literal_eval

import scriptcontext as sc

import compas_rhino
from compas_rhino.forms import TextForm
from compas_ui.session import Session


def match_vertices(cablemesh, keys):
    temp = compas_rhino.get_objects(name="{}.vertex.*".format(cablemesh.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def match_edges(cablemesh, keys):
    temp = compas_rhino.get_objects(name="{}.edge.*".format(cablemesh.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')[2].split('-')
        u = literal_eval(parts[0])
        v = literal_eval(parts[1])
        if (u, v) in keys or (v, u) in keys:
            guids.append(guid)
    return guids


def match_faces(cablemesh, keys):
    temp = compas_rhino.get_objects(name="{}.face.*".format(cablemesh.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def select_vertices(cablemesh, keys):
    guids = match_vertices(cablemesh, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_edges(cablemesh, keys):
    guids = match_edges(cablemesh, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_faces(cablemesh, keys):
    guids = match_faces(cablemesh, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def is_valid_file(filepath, ext):
    """Is the selected path a valid file.

    Parameters
    ----------
    filepath
    """
    if not filepath:
        return False
    if not os.path.exists(filepath):
        return False
    if not os.path.isfile(filepath):
        return False
    if not filepath.endswith(".{}".format(ext)):
        return False
    return True


def select_filepath_open(root, ext):
    """Select a filepath for opening a session.

    Parameters
    ----------
    root : str
        Base directory from where the file selection is started.
        If no directory is provided, the parent folder of the current
        Rhino document will be used
    ext : str
        The type of file that can be openend.

    Returns
    -------
    tuple
        The parent directory.
        The file name.
    None
        If the procedure fails.

    Notes
    -----
    The file extension is only used to identify the type of session file.
    Regardless of the provided extension, the file contents should be in JSON format.

    """
    ext = ext.split('.')[-1]
    filepath = compas_rhino.select_file(folder=root, filter=ext)
    if not is_valid_file(filepath, ext):
        print("This is not a valid session file: {}".format(filepath))
        return
    return filepath


def select_filepath_save(root, ext):
    """Select a filepath for saving a session."""
    filepath = compas_rhino.rs.SaveFileName('save', filter=ext, folder=root)
    if not filepath:
        return
    if filepath.split('.')[-1] != ext:
        filepath = "%s.%s" % (filepath, ext)
    return filepath


def get_FF():
    session = Session()
    if "FF" not in session:
        form = TextForm('Initialise the plugin first!', 'FF')
        form.show()
        return None
    return session["FF"]


def get_scene():
    FF = get_FF()
    if FF:
        return FF['scene']


def get_proxy():
    session = Session()
    if "FF.proxy" not in session:
        form = TextForm('Initialise the plugin first!', 'FF')
        form.show()
        return None
    return session["FF.proxy"]


def get_system():
    session = Session()
    if "FF.system" not in session:
        form = TextForm('Initialise the plugin first!', 'FF')
        form.show()
        return None
    return session["FF.system"]


def compile_session():
    scene = get_scene()
    session = {
        "data": {"cablemesh": None},
        "settings": scene.settings,
    }
    cablemesh = scene.get('cablemesh')[0]
    if cablemesh:
        session['data']['cablemesh'] = cablemesh.datastructure
    return session


def load_session(session_data):
    print("loading session")
    scene = get_scene()
    scene.clear()
    if 'settings' in session_data:
        scene.settings = session_data['settings']
    if 'data' in session_data:
        data = session_data['data']
        if 'cablemesh' in data and data['cablemesh']:
            scene.add(data['cablemesh'], name="cablemesh")
    scene.update()


def record():
    session = Session()
    session.record()


def undo(sender, e):
    session = Session()
    if e.Tag == "undo":
        session.undo()
        load_session(session.data)
        e.Document.AddCustomUndoEvent("FF Redo", undo, "redo")
    if e.Tag == "redo":
        session.redo()
        load_session(session.data)
        e.Document.AddCustomUndoEvent("FF Redo", undo, "undo")


def FF_undo(command):
    def wrapper(*args, **kwargs):
        session = Session()
        sc.doc.EndUndoRecord(sc.doc.CurrentUndoRecordSerialNumber)
        undoRecord = sc.doc.BeginUndoRecord("FF Undo")
        if undoRecord == 0:
            print("undo record did not start")
        else:
            print("Custom undo recording", undoRecord)

        if len(session.history) == 0:
            record()
        command(*args, **kwargs)
        record()
        sc.doc.AddCustomUndoEvent("FF Undo", undo, "undo")
        if undoRecord > 0:
            sc.doc.EndUndoRecord(undoRecord)
    return wrapper
