# Compressive Arch Supported

This example shows how to...

* create an internal compressive arch
* that supports a membrane/cable-net
* understand the sensitivity of q

A prestressed cable net with compressive arch support is one of the main primitive typologies from which many other membrane geometries are composed. It is a basic combination of a mixed form-active structure.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.39.52.png" alt=""><figcaption><p>Ice Ring Roof Munich, by Ackermann und Partner, Schlaich Bergermann Partner, 1967</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.40.06.png" alt=""><figcaption></figcaption></figure>

The following steps show to create such an internal arch-supported CableMesh:

## 1. <img src="../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create CableMesh

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

> **from Meshgrid**
>
> **Number of faces in the X direction: 10 (default)**
>
> **Number of faces in the Y direction: 10 (default)**
>
> **Dimension in the X direction: 10 (default)**
>
> **Dimension in the Y direction: 10 (default)**

Create a CableMesh data structure with the fastest way of a regular default grid in the XY plane.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.40.17.png" alt=""><figcaption></figcaption></figure>

## 2.  Identity Anchors

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Corners, Manual**

Anchor the nodes of the CableMesh at its corners and in the middle of each boundary.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.40.27.png" alt=""><figcaption></figcaption></figure>

## 3.  Force Density Method

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Find the equilibrium form with the Force Density Method (FD) to check the progress.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.40.47.png" alt=""><figcaption></figcaption></figure>

## 4.  Move Nodes

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt=""><figcaption></figcaption></figure></div>

> **Corners**&#x20;
>
> **Z**

Select the corner vertices and move them downwards in the Z direction slightly.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.40.56.png" alt=""><figcaption></figcaption></figure>

Find equilibrium again:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.41.05.png" alt=""><figcaption></figcaption></figure>

## 5.  Scale Force Densities

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Interactive**
>
> **Edge Loop**

Select the edges along the continuous middle line and scale them interactively so that they are in compression. You will have to play a bit with the second reference point as compressive elements are highly sensitive to their q magnitude.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.41.19.png" alt=""><figcaption></figcaption></figure>

After careful interactive scaling...

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.41.29.png" alt=""><figcaption></figcaption></figure>

The CableMesh shapes over a compressive spline.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 18.41.40.png" alt=""><figcaption></figcaption></figure>
