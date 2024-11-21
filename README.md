# COMPAS Formfinder for Rhino

> [!NOTE]
> The current version of COMPAS-FormFinder on the Yak package server is `0.2.75`.
> Note that this is still a pre-release!

![COMPAS FormFinder](compas-FoFin.png)

COMPAS Formfinder for Rhino is a plugin for Rhino 8
that can be used for form-finding tension-only, compression-only,
and mixed tension-compression structures,
using constrained force-density and constrained dynamric relaxation solvers.

## Installation

To install FormFinder, use Rhino's package manager Yak.
To open Yak, type `PackageManager` on the Rhino command line.

![FormFinder installation with Yak](/gitbook/.gitbook/assets/FormFinder_yak.png)

## COMPAS Packages

FormFinder uses the following COMPAS packages:

* [compas](https://github.com/compas-dev/compas)
* [compas_dr](https://github.com/blockresearchgroup/compas_dr)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_session](https://github.com/blockresearchgroup/compas_session)

After installing RhinoVAULT with Yak, these requirements will be installed automatically if necessary.
The tool might be unresponsive during this process.
The packages are installed in a separate virtual environment named `brg-csd`.

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

These commands can be executed at the Rhino Command Prompt (simply start typing the command name),
or using the FormFinder toolbar.

![FormFinder toolbar](/gitbook/.gitbook/assets/FormFinder_toolbar.png)

If the toolbar is not visible after installing FormFinder,
you can load it from the "Toolbars" page.
To open the "Toolbars" page, type `Toolbar` on the Rhino command line...

![Rhino Toolbars](/gitbook/.gitbook/assets/Rhino_toolbars.png)

## Documentation

For further "getting started" instructions, a tutorial, examples, and an detailed description of the individual commands and the user interface, please check out the online documentation here: [FormFinder Gitbook](https://blockresearchgroup.gitbook.io/FormFinder)

## Issues

Please report problems using the issue tracker of the github repo: <https://github.com/blockresearchgroup/compas-FoFin/issues>

## Contributions

If you want to contribute to COMPAS FoFin, check out the [developer guide](https://github.com/BlockResearchGroup/compas-FoFin/wiki/Developer-Guide).
