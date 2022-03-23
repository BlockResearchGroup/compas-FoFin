import os
import sys
import imp
from shutil import copyfile
from subprocess import call

import compas
import compas_rhino
from compas_rhino.install import install as install_packages
from compas_rhino.install_plugin import install_plugin

HERE = os.path.dirname(__file__)
UI = os.path.join(HERE, 'ui')


def install(version='7.0'):
    plugin = os.path.join(UI, 'Rhino', 'FoFin')

    if not os.path.isdir(plugin):
        raise Exception('Cannot find the plugin: {}'.format(plugin))

    plugin_dir = os.path.abspath(plugin)

    # this is a simplified temp duplicate of install_plugin

    plugin_path, plugin_name = os.path.split(plugin_dir)
    plugin_path = plugin_path or os.getcwd()

    plugin_dev = os.path.join(plugin_dir, 'dev')
    plugin_info = os.path.join(plugin_dev, '__plugin__.py')

    __plugin__ = imp.load_source('__plugin__', plugin_info)

    if hasattr(__plugin__, 'packages'):
        install_packages(version=version, packages=__plugin__.packages)

    install_plugin(plugin)

    if compas.WINDOWS:
        ruipy = os.path.join(plugin_dev, 'rui.py')
        ruiname = '{}.rui'.format(plugin_name)
        python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

        call(sys.executable + " " + ruipy, shell=True)
        copyfile(os.path.join(plugin_dev, ruiname), os.path.join(python_plugins_path, '..', '..', 'UI', ruiname))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='FoFin UI installer command line utility.')

    parser.add_argument('--version', default='7.0', choices=['6.0', '7.0'], help="Version of Rhino.")
    args = parser.parse_args()

    install(version=args.version)
