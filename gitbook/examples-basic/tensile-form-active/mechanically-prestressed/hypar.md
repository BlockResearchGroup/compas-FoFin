# Hypar

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.14.59.png" alt=""><figcaption></figcaption></figure>

This example shows how to...

* assign anchors in corners
* move anchors
* scale force densities along the boundary to introduce boundary cables
* to control the shape of a membrane into a hypar geometry.

A hypar is one of the main primitive typologies for membranes from which many other membrane geometries are composed. It is also known as four-point sail or saddle surface.

The first mechanically prestressed membrane was at the Bundesgartenschau in Kassel in 1955 by the pioneer Frei Otto:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.15.34.png" alt=""><figcaption><p>Bundesgartenschau Kassel, 1955 (source: Atelier Frei Otto)</p></figcaption></figure>

Back then, physical form finding with soap films defined the shape in the absence of digital form-finding tools:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.16.17.png" alt=""><figcaption></figcaption></figure>

The following steps show how to create a hypar with compas-FoFin:

## 1. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create MeshGrid

<div align="left" data-full-width="false"><figure><img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

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

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.17.00.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left" data-full-width="false"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Corners**

Anchor its corner vertices so that they can take reaction forces.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.24.56.png" alt=""><figcaption></figcaption></figure>

## 3. <img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt="" data-size="line"> Move Nodes

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt=""><figcaption></figcaption></figure></div>

> **Manual**&#x20;
>
> **Z**

Manually select two opposite corner vertices and move them upwards in the Z direction.&#x20;

{% hint style="success" %}
When moving nodes, you can select between free and constrained directions that allow you to move in a more controlled manner.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.27.17.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Find the equilibrium form with the Force Density Method (FD).&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.27.58.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The equilibrium can be found after any step as long as meaningful anchors are set.&#x20;
{% endhint %}

The shape does correspond neither to the shape of the soap film experiment nor the pavilion structure. This is because there is higher tension in the boundary materialized with an edge cable or edge wire, respectively. So we must increase the force densities in the edges along the free boundaries.

## 5. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Scaling mode: Interactive**
>
> **Selection mode: Boundaries**

Select the edges along the boundary and scale up their force densities (q) interactively by a factor of, e.g., 5.&#x20;

{% hint style="info" %}
You must first set a **Base Point for Scaling**, then a **Reference point 1** and a **Reference Point 2.** Depending on the distance of the base to the first reference point is the sensitivity for scaling to the second reference point. The scaling factor is displayed in Rhino.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.30.51.png" alt=""><figcaption></figcaption></figure>

## 6. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Again find the equilibrium form with FD with the new state of force densities resulting in the target geometry of the hypar.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 11.31.30.png" alt=""><figcaption></figcaption></figure>
