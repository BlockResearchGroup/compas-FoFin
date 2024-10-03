# User Interface

<figure><img src="../.gitbook/assets/FormFinder_toolbar.png" alt="FormFinder toolbar"><figcaption><p>Screenshot of the toolbar of FormFinder in Rhino 8 on Mac.</p></figcaption></figure>

FormFinder defines a series of Rhino commands which can be executed using the Rhino "command prompt" (by simply typing the command name) or through the corresponding toolbar buttons. Below is an overview of the commands and the corresponding buttons.

## FF

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/1_FF.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Display a dialog with some basic information about the tool and links to the documentation.

## FF\_pattern

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Create a force pattern from different types of input.

### RhinoBox

This option requires the following inputs:

* **Rhino DocObject**: An object with a box-like geometry.
* **Resolution U**: The number of faces in the U direction.
* **Resolution V**: The number of faces in the V direction.

### RhinoCylinder

This option requires the following inputs:

* **Rhino DocObject**: An object with a cylinder-like geometry.
* **Resolution U**: The number of faces in the U direction.
* **Resolution V**: The number of faces in the V direction.

### RhinoMesh

This option requires the following inputs:

* **Rhino DocObject**: An object with a mesh geometry.

{% hint style="info" %}
The number of faces of the mesh is taken "as is".
{% endhint %}

### RhinoSurface

This option requires the following inputs:

* **Rhino DocObject**: An object with a single NURBS surface.
* **Resolution U**: The number of faces in the U direction.
* **Resolution V**: The number of faces in the V direction.

### MeshGrid

This option requires the following inputs:

* **X SizeX**: Defaults to 10.
* **Y Size**: Defaults to the value of X Size.
* **X Faces**: Defaults to 10.
* **Y Faces**: Defaults to the value of X Faces.

## FF\_anchors

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Add or remove pattern anchors.

## FF\_solve\_fd

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Solve equilibrium with a constrained, iterative variant of the force density method.

## FF\_anchors\_move

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Move the anchored vertices of the pattern.

## FF\_anchors\_constraints

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Add geometric constraints to the anchored vertices of the pattern.

## FF\_anchors\_update

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/11_FF_anchors_update.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Update the position of the constrained vertices by projecting them onto their constraints.

## FF\_vertices\_attrs

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/12_FF_anchors_attr.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Modify the attributes of selected vertices.

## FF\_edges\_q

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Modify the force densities (`q`) of selected edges. Two options are available.

### Absolute Value

This option overwrites all the values of the selected edges with the provided value.

### Scaling Factor

This option scales the values of the selected edges individually using the provided scale factor.

## FF\_edges\_delete

<div align="left" data-full-width="false">

<figure><img src="../../resources/FF_toolbar_buttons/14_FF_edges_remove.svg" alt="" width="64"><figcaption></figcaption></figure>

</div>

Modify the pattern by removing selected edges.
