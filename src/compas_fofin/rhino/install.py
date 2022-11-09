import os
import sys

from shutil import copyfile
from subprocess import call

import compas
from compas.plugins import plugin
import compas_rhino

from compas_rhino.install_plugin import install_plugin


HERE = os.path.dirname(__file__)


def get_version_from_args():
    args = compas_rhino.INSTALLATION_ARGUMENTS
    return compas_rhino._check_rhino_version(args.version)


@plugin(category="install", tryfirst=True)
def after_rhino_install(installed_packages):
    if "compas_ui" not in installed_packages:
        return []
    if "compas_cloud" not in installed_packages:
        return []
    if "compas_fofin" not in installed_packages:
        return []

    version = get_version_from_args()
    install(version)

    return [("compas_fofin", "FormFinder UI installed", True)]


@plugin(category="install", tryfirst=True)
def installable_rhino_packages():
    return ["compas_fofin"]


def install(version="7.0"):
    plugin_name = "FoFin"
    plugin_path = os.path.join(HERE, "ui", plugin_name)
    if not os.path.isdir(plugin_path):
        raise Exception("Cannot find the plugin: {}".format(plugin_path))

    plugin_path = os.path.abspath(plugin_path)
    plugin_dev = os.path.join(plugin_path, "dev")

    install_plugin(plugin_path)

    if compas.WINDOWS:
        plugin_ruipy = os.path.join(plugin_dev, "rui.py")
        plugin_rui = "{}.rui".format(plugin_name)
        python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

        call(sys.executable + " " + plugin_ruipy, shell=True)
        copyfile(
            os.path.join(plugin_dev, plugin_rui),
            os.path.join(python_plugins_path, "..", "..", "UI", plugin_rui),
        )


if __name__ == "__main__":

    print("This installation procedure is deprecated.")
    print("Use `python -m compas_rhino.install` instead.")
