import os
import sys
import json
from shutil import copyfile
from subprocess import call

import compas
from compas.plugins import plugin
import compas_rhino
from compas_rhino.install import install as install_packages
from compas_rhino.install import _filter_installable_packages
from compas_rhino.install_plugin import install_plugin


HERE = os.path.dirname(__file__)

# Split up the installation process into smaller parts
# TODO: check that all folders are where they were expected
# TODO: check that user has write access to all required folders
# TODO: check that all required packages are available in the current env
# TODO: install all packages for Rhino (not just required)
# TODO: remove old versions of the plugin
# TODO: remove old versions of the rui file
# TODO: install the plugin
# TODO: install the rui file
# TODO: use a proper logger


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
    plugin_config = os.path.join(plugin_dev, "config.json")

    with open(plugin_config, "r") as f:
        config = json.load(f)

    packages = []
    packages = _filter_installable_packages(version, packages)

    if "packages" in config:
        for name in config["packages"]:
            if name not in packages:
                packages.append(name)

    install_packages(version=version, packages=packages)
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
    import argparse

    parser = argparse.ArgumentParser(
        description="COMPAS FormFinder installer command line utility."
    )
    parser.add_argument(
        "--version",
        default="7.0",
        choices=["6.0", "7.0"],
        help="Version of Rhino.",
    )
    args = parser.parse_args()

    install(version=args.version)
