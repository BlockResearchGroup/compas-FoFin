# COMPAS Formfinder for Rhino

![COMPAS FormFinder](compas-FoFin.png)

COMPAS Formfinder for Rhino is a plugin for Rhino 8
that can be used for form-finding tension-only, compression-only,
and mixed tension-compression structures,
using constrained force-density and constrained dynamric relaxation solvers.

## Installation

The plugin can be installed using Rhino's package manager Yak.

![COMPAS FormFinder installation with Yak](compas-FoFin_installation.png)

## COMPAS Packages

The plugin is based on COMPAS and written entirely in Python.
It uses the following packages of the COMPAS framework:

* [compas](https://github.com/compas-dev/compas)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_dr](https://github.com/blockresearchgroup/compas_dr)

Note that, at least for now, these packages have to be installed separately from the plugin itself.
This can be done as described in the COMPAS docs (see ...),
or using the Python3 shell available in the Rhino ScriptEditor.

## Documentation

The functionality of the plugin is documented in this gitbook: <https://blockresearchgroup.gitbook.io/compas-fofin>

## Issues

Please report problems using the issue tracker of the github repo: <https://github.com/BlockResearchGroup/compas-FoFin/issues>
