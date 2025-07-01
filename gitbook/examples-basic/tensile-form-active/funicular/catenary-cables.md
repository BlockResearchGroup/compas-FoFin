# Catenary Cables

This example shows how to...

* select all edges in either U or V (warp or weft)
* set force densities to a specific value
* apply external loads
* to generate a funicular parabolic geometry.

A catenary cable under its own self-weight is the most primitive typology for a form-active structure. For its form finding one must solely let any cable, rope, or chain hang. Its simple yet elegant shape finds application in iconic architecture.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.16.png" alt=""><figcaption><p>Washington Dulles International Airport, Eero Saarinen, 1962</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.27.png" alt=""><figcaption><p>Poleni’s drawing of Hooke’s analogy between an arch and a hanging chain</p></figcaption></figure>

## 1. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create CableMesh

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

Create a CableMesh data structure with the fastest way of a regular default grid in the XY plane.\


<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.52.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **ByContinuousEdges**

Constraint its two opposing boundary vertices so that they can take reaction forces.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.07.png" alt=""><figcaption></figcaption></figure>

## 3. <img src="../../../../resources/FF_toolbar_buttons/12_FF_anchors_attr.svg" alt="" data-size="line"> Edge Attributes

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> Value
>
> Edge Loop

Select all edges perpendicular to the ones connecting the supports and set the force densities q to a number close to 0 (0.0001).&#x20;

{% hint style="danger" %}
It is numerically not possible to set q to 0.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.30.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Finding the equilibrium will not change the geometry of the Cablemesh as there is uni-axial prestress and no loads applied yet.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.42.png" alt=""><figcaption></figcaption></figure>

## 5. <img src="../../../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt="" data-size="line"> Vertices Attributes&#x20;

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt=""><figcaption></figcaption></figure></div>

> **All**
>
> **Thickness = 0.1**

Select all nodes and apply a uniform thickness of 0.1. The forces will be calculated based to the tributary area of each node.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-07-01 at 15.53.46.png" alt=""><figcaption></figcaption></figure>

After running the force density method, the two boundary edges will have higher forces compared to the rest, so the two boundary arches will be more shallow. This happens because the tributary area of the nodes on the boundaries is half compared to the nodes in the middle of the cable mesh. So, in the next step we have to scale the q values on the boundaries by 0.5:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-07-01 at 15.53.25.png" alt=""><figcaption></figcaption></figure>

## 7. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Scale Force Density

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

Select the two boundary edges and scale the q values to 0.5:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-07-01 at 15.57.50.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-07-01 at 15.59.29.png" alt=""><figcaption></figcaption></figure>

## 7. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> &#x20;**Interactive**
>
> All

Scale the edges connecting the supports in the hanging cable direction interactively until reaching your target design (alternatively, you can use a scale factor applied to all the edges):

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.32.png" alt=""><figcaption></figcaption></figure>
