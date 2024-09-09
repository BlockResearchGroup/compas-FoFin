# COMPAS Formfinder for Rhino

![COMPAS FormFinder](compas-FoFin.png)

COMPAS Formfinder for Rhino is a plugin for Rhino 8
that can be used for form-finding tension-only, compression-only,
and mixed tension-compression structures,
using constrained force-density and constrained dynamric relaxation solvers.

> [!WARNING]  
> This plugin is under active development,
> and uses the still somewhat unstable CPython infrastructure
> of Rhino 8 through the new ScriptEditor.
> Therefore, unexpected errors may occur here and there.
> Please let us know via the [Issue Tracker](https://github.com/BlockResearchGroup/compas-FoFin/issues) if you have problems.

## Installation

The plugin can be installed using Rhino's package manager Yak.

![COMPAS FormFinder installation with Yak](resources/images/FormFinder_yak.png)

## COMPAS Packages

The plugin is based on COMPAS and written entirely in Python.
It uses the following packages of the COMPAS framework:

* [compas](https://github.com/compas-dev/compas)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_dr](https://github.com/blockresearchgroup/compas_dr)
* [compas_rui](https://github.com/blockresearchgroup/compas_rui)
* [compas_session](https://github.com/blockresearchgroup/compas_session)

Note that, at least for now, these packages have to be installed separately from the plugin itself.
This can be done as described in the COMPAS docs (see [Working in Rhino 8](https://compas.dev/compas/latest/userguide/cad.rhino8.html)).

> [!WARNING]  
> We recommend using `pip` based install exclusively,
> and not mix this installation mechanism with the `# r: package`
> syntax available for CPython scripts in the new Rhino ScriptEditor,
> since this can result in duplicated package installations with incompatible versions.

## User Interface

COMPAS FormFinder defines the following Rhino commands:

* `FF`
* `FF_pattern`
* `FF_anchors`
* `FF_anchors_constraints`
* `FF_anchors_update`
* `FF_anchors_move`
* `FF_solve_fd`
* `FF_edges_q`
* `FF_edges_delete`
* `FF_vertices_attrs`
* `FF_edges_attrs`
* `FF_session_undo`
* `FF_session_redo`
* `FF_session_open`
* `FF_session_save`
* `FF_scene_clear`
* `FF_scene_redraw`
* `FF_settings`
* `FF_reqs_check`
* `FF_reqs_install`

These commands can be executed at the Rhino Command Prompt (simply start typing the command name),
or using the RhinoVAULT toolbar.

![FormFinder toolbar](resources/images/FormFinder_toolbar.png)

## Documentation

For further "getting started" instructions, a tutorial, examples, and an detailed description of the individual commands and the user interface, please check out the online documentation here: [FormFinder Gitbook](https://blockresearchgroup.gitbook.io/FormFinder)

## Issues

Please report problems using the issue tracker of the github repo: <https://github.com/blockresearchgroup/compas-FoFin/issues>
