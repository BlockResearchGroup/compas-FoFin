# Catenary Cables

This example shows how to...

* select all edges in either U or V (warp or weft)
* set force densities to a specific value
* apply external loads
* to generate a funicular parabolic geometry.

A catenary cable under its own self-weight is the most primitive typology for a form-active structure. For its form finding one must solely let any cable, rope, or chain hang. Its simple yet elegant shape finds application in iconic architecture.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.16.png" alt=""><figcaption><p>Washington Dulles International Airport, Eero Saarinen, 1962</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.27.png" alt=""><figcaption><p>Poleni’s drawing of Hooke’s analogy between an arch and a hanging chain</p></figcaption></figure>

{% hint style="danger" %}
The example is simplified to a constant external load and does not use self-weight computed based on the tributary area of each node. This will be introduced in the advanced examples. So basically the shape is a parabola as the force applied is uniform with respect to horizontal distance.
{% endhint %}

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

Select all edges connecting the supports and set the force densities q to a number close to 0 (0.0001).&#x20;

{% hint style="danger" %}
It is numerically not possible to set q to 0.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.30.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Finding the equilibrium will not change the geometry of the Cablemesh as there is uni-axial prestress and no loads applied yet.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.42.png" alt=""><figcaption></figcaption></figure>

## 5. <img src="../../../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt="" data-size="line"> Node Attributes&#x20;

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt=""><figcaption></figcaption></figure></div>

> **All**
>
> **pz = -1.0**

Select all nodes and apply a uniform point load of -1.0 in the negative Z direction with the **pz** attribute.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.51.54.png" alt=""><figcaption></figcaption></figure>

The external loads are displayed with green arrows:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.06.png" alt=""><figcaption></figcaption></figure>

## 6. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

The system finds a funicular shape that is hanging down much because the ratio of forces to force densities is relatively high:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.20.png" alt=""><figcaption></figcaption></figure>

## 7. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> &#x20;**Interactive**
>
> Edge Loop

Scale the edges connecting the supports in the hanging cable direction interactively until reaching your target design:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.32.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.43.png" alt=""><figcaption></figcaption></figure>
