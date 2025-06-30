# Conical

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.41.04.png" alt=""><figcaption></figcaption></figure>

This example shows how to...

* select anchors by boundaries and manual selection and unselect anchors
* modify the topology of the CableMesh
* move anchors
* tweak force densities&#x20;
* to control a shape of a membrane into a conical geometry with a light-eye.

The conical membrane is one of the main primitive typologies for membranes from which many other membrane geometries are composed. It can come with a single anchor point (however this results in high stress concentrations), a circular fixed boundary, or a single anchor with an eye-shaped opening.

The German Pavillion of the World Expo in 1967 in Montreal by Frei Otto and Rolf Gutbrod is a good example for the eye-shaped design.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.41.42.png" alt=""><figcaption></figcaption></figure>

Back then, physical form finding with soap films and stockings defined the shape in the absence of digital form-finding tools:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.41.58.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.42.13.png" alt=""><figcaption></figcaption></figure>

The following steps show how to create such a conical membrane with COMPAS-FormFinder:

## 1. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create MeshGrid

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

> **from Meshgrid**
>
> **Number of faces in the X direction: 10 (default)**
>
> **Number of faces in the Y direction: 10 (default)**
>
> **Dimension in the X direction: 10 (default)**
>
> **Dimension in the Y direction: 10 (default)**

Create a MeshGrid data structure with the fastest way of a regular default grid in the XY plane.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.42.28.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Boundaries, Manual**

Anchor its boundary nodes and a node in the centre of the mesh.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.42.40.png" alt=""><figcaption><p>boundaries</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.42.49.png" alt=""><figcaption><p>manual</p></figcaption></figure>

## 3. <img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt="" data-size="line"> Move Nodes

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt=""><figcaption></figcaption></figure></div>

> **Manual**
>
> **Z**

Move the centre node upwards in the Z direction.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.42.59.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Find the equilibrium form with the Force Density Method (FD).

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.09.png" alt=""><figcaption></figcaption></figure>

## 5. <img src="../../../../resources/FF_toolbar_buttons/14_FF_edges_remove.svg" alt="" data-size="line"> **Remove** Edges&#x20;

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/14_FF_edges_remove.svg" alt=""><figcaption></figcaption></figure></div>

> **Manual**

Delete edges in the centre in the adjacency of the anchor.&#x20;

{% hint style="info" %}
Deleting edges of the CableMesh will also delete the adjacent faces (that by default are not shown) and the resulting unused nodes.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.18.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.27.png" alt=""><figcaption></figcaption></figure>

## 6. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Again find the equilibrium form with FD with the new topology resulting in the smooth light-eye opening in the centre.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.38.png" alt=""><figcaption></figcaption></figure>

## 7. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Interactive**
>
> &#x20;**Boundaries**

Select all boundary edges and scale their force densities by a factor of e.g. 5. The anchored boundary will not be affected by this modification.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.48.png" alt=""><figcaption></figcaption></figure>

## 8. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Again find the equilibrium form with FD with force densities along the boundaries that would be materialized as edge cables.&#x20;

With the value of q set to 5 on the boundaries the light-eye becomes small:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.43.58.png" alt=""><figcaption></figcaption></figure>

For comparison, the light-eye becomes large for the q's on the boundaries set to 0.5:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.44.07.png" alt=""><figcaption></figcaption></figure>

## 9. <img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Unselect**
>
> **Manual**

Manually unselect anchors along the outer boundary so that the design approximates the Expo Pavilion.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.44.17.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.44.29.png" alt=""><figcaption></figcaption></figure>

## 10. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

The equilibrium shape results in the following design:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.44.39.png" alt=""><figcaption></figcaption></figure>
