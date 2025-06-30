# Catenary Arch with Corrugations

This example is a continuation of the example on generating a tensile [funicular](broken-reference) geometry.&#x20;

This example shows how to...

* flip force densities from positive to negative values to create compressive instead of tensile forces in the edges
* to thus form find a compression-only funicular structure
* and create corrugations by scaling force densities.

"As hangs a flexible cable so, inverted, stand the touching pieces of an arch." Robert Hook

Following this rule, the force densities must just be inverted in sign to turn them from tension to compression and vice versa. So the catenary hanging cables under self-weight get turned into a catenary barrel vault.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 14.50.27.png" alt=""><figcaption><p>Poleni’s drawing of Hooke’s analogy between an arch and a hanging chain</p></figcaption></figure>

This principle has been applied already in ancient construction:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.39.39.png" alt=""><figcaption><p>Ctesiphon Arch, Iraq</p></figcaption></figure>

Funicular barrel vaults can also be corrugated as a stiffening scheme:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.39.52.png" alt=""><figcaption><p>Navíos Corporation Silos, Eladio Dieste<br></p></figcaption></figure>

This example shows you how to create a funicular barrel vault and extend it with corrugations:

### 1. Load Session <a href="#id-1.-load-session" id="id-1.-load-session"></a>

<div align="left"><figure><img src="../../.gitbook/assets/2_FF_open.svg" alt="" width="38"><figcaption></figcaption></figure></div>

Load the session file of the hanging cables example in pure tension:\


{% file src="../../.gitbook/assets/ex_funicolar_tension.json" %}

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 14.52.43.png" alt=""><figcaption></figcaption></figure>

## 2. <img src="broken-reference" alt="" data-size="line"> Scale Force Densities

> **Value**
>
> Edge Loop
>
> **-4**

In order to turn tensile edges into compressive edges, the force densities must have a negative value. Select the edges connecting the supports and scale them by a factor of -4 to invert the sense of force in the edges.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.40.23.png" alt=""><figcaption></figcaption></figure>

## Introduce Corrugations

Corrugations can be created by alternating high and low force densities in the cables. Cables with lower forces have higher rise,  cables with higher forces have lower rise.&#x20;

## 3. <img src="broken-reference" alt="" data-size="line"> Scale Force Densities

> **Interactive**
>
> **Edge Loop**

Select alternating loops of edges connecting the supports:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.40.35.png" alt=""><figcaption></figcaption></figure>

The interactive scaling of force densities allows tweaking your design intuitively:

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.40.45.png" alt=""><figcaption></figcaption></figure>

The equilibrium shape will have corrugations with arches alternatively carrying low and high forces.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-30 at 16.40.56.png" alt=""><figcaption></figcaption></figure>
