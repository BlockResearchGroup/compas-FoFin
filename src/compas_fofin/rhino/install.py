import os
import sys
import imp
import json
from shutil import copyfile
from subprocess import call

import compas
from compas.plugins import plugin
import compas_rhino
from compas_rhino.install import install as install_packages
from compas_rhino.install_plugin import install_plugin


HERE = os.path.dirname(__file__)


@plugin(category="install", tryfirst=True)
def installable_rhino_packages():
    return ["compas_fofin"]


def install(version="7.0"):
    plugin = os.path.join(HERE, "ui", "FoFin")

    if not os.path.isdir(plugin):
        raise Exception("Cannot find the plugin: {}".format(plugin))

    plugin_dir = os.path.abspath(plugin)

    plugin_path, plugin_name = os.path.split(plugin_dir)
    plugin_path = plugin_path or os.getcwd()
    plugin_dev = os.path.join(plugin_dir, "dev")
    plugin_config = os.path.join(plugin_dev, "config.json")

    with open(plugin_config, "r") as f:
        config = json.load(f)

    if "packages" in config:
        install_packages(version=version, packages=config["packages"])

    install_plugin(plugin)

    if compas.WINDOWS:
        ruipy = os.path.join(plugin_dev, "rui.py")
        ruiname = "{}.rui".format(plugin_name)
        python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

        call(sys.executable + " " + ruipy, shell=True)
        copyfile(
            os.path.join(plugin_dev, ruiname),
            os.path.join(python_plugins_path, "..", "..", "UI", ruiname),
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="FoFin UI installer command line utility."
    )
    parser.add_argument(
        "--version", default="7.0", choices=["6.0", "7.0"], help="Version of Rhino."
    )
    args = parser.parse_args()

    install(version=args.version)
