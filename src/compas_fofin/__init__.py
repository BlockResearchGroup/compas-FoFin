from __future__ import print_function

import os

__author__ = ["tom van mele"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch"
__version__ = "0.13.0"

title = "FormFinder"
designers = ["Juney Lee"]
developers = ["Tom Van Mele", "Li Chen"]
documenters = ["Petras Vestartas"]
description = """
"""
website = "https://gitbook.com/blockresearchgroup/compas-Fofin"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    "compas_fofin.rhino.install",
    "compas_fofin.rhino.scene",
]
