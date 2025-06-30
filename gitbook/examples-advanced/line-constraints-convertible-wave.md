# Line Constraints - Convertible Wave

This example builds upon the basic example of the [Ridge Valley Wave](broken-reference) and shows how to...

* introduce anchor constraints to a line in order to design a convertible structure where the reaction forces are perpendicular to a rail only.

{% file src="../.gitbook/assets/Wave.json" %}

## 1. Open the example file

<div align="left" data-full-width="false"><figure><img src="../.gitbook/assets/2_FF_open.svg" alt="" width="38"><figcaption></figcaption></figure></div>

Supports on a sliding rail can only take reaction forces perpendicular to the rail line. Thus the system must find a new equilibrium shape where the anchors can slide on line constraints.

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 21.57.20.png" alt=""><figcaption></figcaption></figure>

## 2. Add Line constraints

<div align="left"><figure><img src="../../resources/FF_toolbar_buttons/10_FF_anchors_modify.svg" alt=""><figcaption></figcaption></figure></div>

`Anchors_constraints  > Add > Manual`

Manually select the anchors that belong to the same line constraint and assign the line constraint to them. Once you press done, the line and the selected anchors becomes cyan.

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.01.45.png" alt=""><figcaption></figcaption></figure>

Repeat the same command sequence for each constraint marked with the black arrow.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.09.17.png" alt=""><figcaption></figcaption></figure>

## 3. Further Opening up of the Convertible

<div align="left"><figure><img src="../../resources/FF_toolbar_buttons/9_FF_anchors_move.svg" alt=""><figcaption></figcaption></figure></div>

### &#x20;`Anchors_move > Y > Manual`

The convertible roof can be opened up further by "pulling" a pair of corner anchors along the line (in the current example, in the Y direction).&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-06-30 at 22.14.53.png" alt=""><figcaption></figcaption></figure>
