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


def plugin_devpath(name):
    plugin = os.path.join(HERE, "ui", name)
    if not os.path.isdir(plugin):
        raise Exception("Cannot find the plugin: {}".format(plugin))

    plugin_dir = os.path.abspath(plugin)
    plugin_path, plugin_name = os.path.split(plugin_dir)
    plugin_path = plugin_path or os.getcwd()
    return os.path.join(plugin_dir, "dev")


def install(version="7.0"):
    name = "FoFin"
    dev = plugin_devpath(name)
    config = os.path.join(dev, "config.json")

    with open(config, "r") as f:
        config = json.load(f)

    packages = []
    packages = _filter_installable_packages(version, packages)

    if "packages" in config:
        for name in config["packages"]:
            if name not in packages:
                packages.append(name)

    install_packages(version=version, packages=packages)
    install_plugin(plugin)

    if compas.WINDOWS:
        ruipy = os.path.join(dev, "rui.py")
        ruiname = "{}.rui".format(name)
        python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

        call(sys.executable + " " + ruipy, shell=True)
        copyfile(
            os.path.join(dev, ruiname),
            os.path.join(python_plugins_path, "..", "..", "UI", ruiname),
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
