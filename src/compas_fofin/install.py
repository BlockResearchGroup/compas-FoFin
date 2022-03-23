import os

HERE = os.path.dirname(__file__)
UI = os.path.join(HERE, 'ui')


def install(environment='Rhino', version='7.0'):
    if environment != 'Rhino':
        raise NotImplementedError

    path = os.path.join(UI, environment, 'FoFin')
    devpath = os.path.join(path 'dev')
    # from devpath import __plugin__
    # load required packages
    # run rhino install command with required packages
    # run rhino install plugin command with path
    # on windows
    # compile rui folder
    # copy rui folder into rhino default folder
    # report
