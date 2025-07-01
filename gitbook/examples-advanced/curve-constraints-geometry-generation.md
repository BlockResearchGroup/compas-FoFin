# Curve Constraints - Geometry Generation

This example shows how to ...

* create a geometry based on curve constraints as boundary
* so that the cable net finds equilibrium with reaction forces acting normal only to the boundary curves.&#x20;

This geometry was designed and materialized in a [research project](https://block.arch.ethz.ch/brg/project/cable-net-fabric-formed-thin-shell-buda-tx-usa) by the BRG together with Escobedo Construction in 2014 in Texas.

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.22.25.png" alt=""><figcaption><p>.Cable-net and fabric formed thin shell, Buda, TX, USA, 2014</p></figcaption></figure>

## 0. Input

Start with the target boundary curves by opening the Rhino File:

{% file src="../.gitbook/assets/texas_boundary_r7.3dm" %}

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.23.53.png" alt=""><figcaption></figcaption></figure>

## 1.  Create CableMesh

> **from RhinoSurface**
>
> **Number of faces in the U direction: 9**
>
> **Number of faces in the V direction: 19**

Create a CableMesh data structure from a planar Rhino surface that spans between the endpoints of the curves.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.24.04.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.24.15.png" alt=""><figcaption></figcaption></figure>

## 2. Identify Anchors

<div align="left" data-full-width="false"><figure><img src="../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Boundary**

Anchor its corner vertices along the boundary.

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.24.26.png" alt=""><figcaption></figcaption></figure>

## 3.  Set Anchor Constraints

<div align="left"><figure><img src="../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**
>
> **By Continuous Edges**

Select the anchors along continuous edges along the boundary and constrain them to the respective target boundary curve. Pay attention to not select the vertices in the corner, but only the ones in between corners.

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.24.35.png" alt=""><figcaption></figcaption></figure>

## 4.  Force Density Method

<div align="left"><figure><img src="../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

The CableMesh can now be form found with the Force Density method.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-07-01 at 16.37.31.png" alt=""><figcaption></figcaption></figure>
