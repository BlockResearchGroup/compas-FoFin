# Selecting Vertices

Many of the commands of COMPAS FormFinder operate on a selection of vertices. Vertices can be selected in various ways.

{% hint style="info" %}
If any of the mechanisms described below don't work as advertised, please file an issue on the [Issue Tracker](https://github.com/BlockResearchGroup/compas-FoFin/issues) describing the problem.
{% endhint %}

## All

Select all vertices of the pattern.

## Boundary

Select all vertices which are on a boundary.

{% hint style="info" %}
Note that you have to switch the Rhino display mode to "Shaded" to see the boundaries of the pattern mesh.
{% endhint %}

## Degree

Select all vertices which have a specific degree. The degree of a vertex is defined as the number of connected vertices of that vertex. For example, in a quad mesh:

* Corners have `degree = 2`
* Other boundary vertices have `degree = 3`
* Internal vertices have `degree = 4`

## EdgeLoop

Select all vertices on the same edge loop.

## Manual

Manually select any set of vertices of the mesh pattern.
