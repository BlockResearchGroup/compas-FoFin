# Getting Started

COMPAS FormFinder is a plugin for Rhino 8. It uses the CPython runtime that is newly available in Rhino 8, and can only be installed using the package manager Yak.

{% hint style="warning" %}
COMPAS FormFinder is **only available for Rhino 8.**
{% endhint %}

## Requirements

* [Rhino 8](https://www.rhino3d.com/)

## Installation

* Start Rhino 8 and launch Yak by typing `PackageManager` on the Rhino command line.
* Search the online packages for "FormFinder".
* Select "COMPAS FormFinder" from the list.
* Install.

<figure><img src="/gitbook/.gitbook/assets/FormFinder_yak.png" alt="FormFinder in package manager Yak"><figcaption><p>COMPAS FormFinder can be installed using Yak, the package manager of Rhino.</p></figcaption></figure>

## COMPAS Packages

FormFinder uses the following COMPAS packages:

* [compas](https://github.com/compas-dev/compas)
* [compas_dr](https://github.com/blockresearchgroup/compas_dr)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_rui](https://github.com/blockresearchgroup/compas_rui)
* [compas_session](https://github.com/blockresearchgroup/compas_session)

After installing RhinoVAULT with Yak, these requirements will be installed automatically if they are not yet available.
Note that the tool ,ight be unresponsive for a few seconds while this happens.
The packages are installed in a separate virtual environment named `formfinder`.

## Toolbar

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

<figure><img src="/gitbook/.gitbook/assets/FormFinder_toolbar.png" alt="COMPAS FormFinder toolbar"><figcaption><p>COMPAS FormFinder commands are available via the toolbar.</p></figcaption></figure>

If the toolbar is not visible after installing FormFinder,
you can load it from the "Toolbars" page.
To open the "Toolbars" page, type `Toolbars` on the Rhino command line...

<figure><img src="/gitbook/.gitbook/assets/Rhino_toolbars.png" alt="Rhino Toolbars page"><figcaption><p>Load the toolbar using the "Toolbars" page.</p></figcaption></figure>

## Check the Installation

To check the installation, simply press the left-most button on the toolbar.
This will install any missing COMPAS packages and display a "Splash" screen when the installation is completed.
Close the screen by agreeing to the [legal terms](../additional-information/legal-terms.md) of using COMPAS-FormFinder.

Note that installing the packages (and the dependencies of the packages) may take some time,
so don't worry if the the dialog doesn't pop up immediately...

<figure><img src="/gitbook/.gitbook/assets/FormFinder_splash.png" alt="FormFinder splash"><figcaption><p>Once all missing COMPAS packages and their dependencies are installed, a "Splash" screen pops up.</p></figcaption></figure>
