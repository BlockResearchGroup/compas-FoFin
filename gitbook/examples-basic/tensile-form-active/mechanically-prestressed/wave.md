# Wave

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.19.02.png" alt=""><figcaption></figcaption></figure>

This example shows how to...

* assign anchors manually
* move anchors
* scale force densities along continuous inner edges to introduce integrated ridge and valley cables
* to control the shape of a membrane into a ridge and valley wave geometry.

A wave is one of the main primitive typologies for membranes from which many other membrane geometries are composed. It is also called a ridge valley wave.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.19.20.png" alt=""><figcaption><p>convertible membrane roofing Metzgergasse, Buchs</p></figcaption></figure>

## 1. <img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create CableMesh

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

> **from Meshgrid**
>
> **Dimension in the X direction: 10 (default)**
>
> **Dimension in the Y direction: 10 (default)**
>
> **Number of faces in the X direction: 20 (default)**
>
> **Number of faces in the Y direction: 20 (default)**

Create a CableMesh data structure with the fastest way of a regular default grid in the XY plane. Choose a higher density e.g. of 20 to enable more design freedom in creating ridges and valleys.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.19.31.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select**&#x20;
>
> **Manual**

Manually select vertices with equal spacing along two boundary sides in between which ridge and valley "cables" will span.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.19.42.png" alt=""><figcaption></figcaption></figure>

## 3. <img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt="" data-size="line"> Move Nodes

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt=""><figcaption></figcaption></figure></div>

> **Manual**&#x20;
>
> **Z**

Manually select alternating vertices along the boundary sides and move them upwards in the Z direction.&#x20;

{% hint style="success" %}
When moving nodes, you can select between free and constrained directions that allow you to move in a more controlled manner.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.19.53.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Find the equilibrium form with the Force Density Method (FD) to check the intermediate state.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.20.04.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The equilibrium can be found after any step as long as meaningful anchors are set.&#x20;
{% endhint %}

The shape is not defined yet by clear ridges and valleys. This is because integrated cables with higher tension will define the articulation. Thus we must increase the force densities along continuous edges.

## 5. <img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Scale Force Densities

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Interactive**
>
> **Continuous**

Select all continuous edges spanning in between the anchor and scale up their force densities q interactively, e.g., by a factor of 10.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.20.14.png" alt=""><figcaption></figcaption></figure>

## **6**. <img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

Again find the equilibrium form with FD with the new state of force densities resulting in the target geometry of the ridge valley wave.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-06-30 at 13.20.25.png" alt=""><figcaption></figcaption></figure>
