# Vault with Lips

This example shows how to...

* create a compression-only funicular vault
* under self-weight
* with lip articulations along the boundaries.&#x20;

Heinz Isler is one of the pioneers that build funicular concrete shells. In the absence of digital form-finding tools, he utilized physical form finding to design his structures.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.26.43.png" alt=""><figcaption><p>Tennishalle in Allschwil, Heinz Isler</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.26.54.png" alt=""><figcaption></figcaption></figure>

## 1.  <img src="../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt="" data-size="line"> Create CableMesh

> **from Meshgrid**

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/6_FF_pattern.svg" alt=""><figcaption></figcaption></figure></div>

Create a CableMesh from a Meshgrid. It could also be an elongated rectangle.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.27.11.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt="" data-size="line"> Identity Anchors

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/7_FF_anchors.svg" alt=""><figcaption></figcaption></figure></div>

> **Select > Corners**

Set anchors at all corner nodes.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.27.25.png" alt=""><figcaption></figcaption></figure>

## 3.  Form finding

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

The edges of the CableMesh are by default in tension (red).

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.27.36.png" alt=""><figcaption></figcaption></figure>

## 4. <img src="../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Edges Scale Force Densities

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **All > -1**

Turn all tensile edges into compressive edges by multiplying the force densities q with the factor of -1.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.27.48.png" alt=""><figcaption></figcaption></figure>

## 5.  Form finding&#x20;

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

The shape of the flat CableMesh without external loads does not change when changing from tension to compression:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.27.59.png" alt=""><figcaption></figcaption></figure>

## 6. <img src="../../../resources/FF_toolbar_buttons/12_FF_anchors_attr.svg" alt="" data-size="line"> Load

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/12_FF_anchors_attr.svg" alt=""><figcaption></figcaption></figure></div>

> **All**

The application of the self-weight should compute the value of `_pz` node attribute based on the tributary area of the node. However, this function is currently not implemented. So,  using the "vertices\_attributes" button, we select all the vertices and assign a \_pz value equal to -0.1 each.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.28.10.png" alt=""><figcaption></figcaption></figure>

## **7**. <img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.28.24.png" alt=""><figcaption></figcaption></figure>

## 8. <img src="../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt="" data-size="line"> Edges Scale Force Densities

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/13_FF_edges_q.svg" alt=""><figcaption></figcaption></figure></div>

> **Edge Loop**

Select edges where you want the lips creases to be and also select the edges connecting the anchors.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.28.35.png" alt=""><figcaption></figcaption></figure>

Then scale up the force densities dynamically or set a negative q value e.g. -3:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.28.47.png" alt=""><figcaption></figcaption></figure>

## 9. <img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt="" data-size="line"> Force Density Method

<div align="left"><figure><img src="../../../resources/FF_toolbar_buttons/8_FF_fd.svg" alt=""><figcaption></figcaption></figure></div>

This results in a vault with lips.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 17.28.59.png" alt=""><figcaption></figcaption></figure>
