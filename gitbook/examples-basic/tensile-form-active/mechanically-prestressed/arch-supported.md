# Arch supported

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.38.04.png" alt=""><figcaption></figcaption></figure>

This example shows how to...

* start from a cylinder
* assign anchors along the boundaries
* scale force densities in the UV directions
* delete edges
* to create the shape of an arch-supported membrane.

An arc-supported membrane is one of the main primitive typologies for membranes from which many other membrane geometries are composed.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.38.17.png" alt=""><figcaption><p>arc-supported membranes, Poruklu Marina</p></figcaption></figure>

The following steps show how to create a arch-supported membrane with compas-FoFin:

## 0. Create Rhino Cylinder

Create a Rhino Cylinder Object with the **Cylinder** command:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.38.34.png" alt=""><figcaption></figcaption></figure>

## 1. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create CableMesh

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

> **from RhinoCylinder**
>
> **Number of faces along perimeter: 16 (default)**
>
> **Number of faces along height: 4 (default)**

Transform the Rhino Cylinder into a CableMesh with the from RhinoCylinder option.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.38.55.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Boundary**

Anchor its nodes on the two boundaries so that they can take reaction forces.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.39.06.png" alt=""><figcaption></figcaption></figure>

## 3. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Find the equilibrium form with the Force Density Method (FD).&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.39.19.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Interactive**
>
> **UV**

Select all continuous edges in one direction, either U or V and scale them interactively.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.39.32.png" alt=""><figcaption></figcaption></figure>

The higher the qs in the longitudinal direction relative to the hoop direction the straighter the cylinder:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.39.45.png" alt=""><figcaption></figcaption></figure>

The lower the qs in the longitudinal direction relative to the hoop direction the more narrow-waisted becomes the cylinder:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.39.59.png" alt=""><figcaption></figcaption></figure>

This is a closed-arch supported membrane. To form find an arch-supported membrane, the topoly of the CableMesh must be modified.

## 5. <img src="../../../../resources/FF_toolbar_buttons/14_FF_edges_remove.svg" alt="" data-size="line"> **Delete** Edges&#x20;

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/14_FF_edges_remove.svg" alt=""><figcaption></figcaption></figure></div>

> **Manual**

Delete all edges of one side of the cylinder.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.40.23.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.40.38.png" alt=""><figcaption></figcaption></figure>

The current release does not allow you to rotate the session file yet, so just rotate your viewport by 90 degrees:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.40.50.png" alt=""><figcaption></figcaption></figure>

## 6. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Interactive**
>
> **Continuous**

Scale the free boundary edges to pull them down with "edge cables":

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.41.03.png" alt=""><figcaption></figcaption></figure>

This results in the anticipated arch-supported membrane design:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.41.15.png" alt=""><figcaption></figcaption></figure>
