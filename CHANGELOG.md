# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.14.0] 2024-10-23

### Added

* Added `compas_fofin.solvers.interactivescalefd.AutoUpdateFD`.
* Added `compas_fofin.solvers.interactivescalefd.InteractiveScaleFD`.
* Added "Interactive" option to `FF_edges_q`.
* Added `compas_fofin.session.FoFinSession`.
* Added `compas_fofin.session.FoFinSession.settings`.
* Added `compas_fofin.scene.RhinoCableMeshObject.edges_conduit`.
* Added `compas_fofin.scene.RhinoCableMeshObject.mesh_conduit`.
* Added `compas_fofin.scene.RhinoCableMeshObject.reactions_conduit`.
* Added `compas_fofin.scene.RhinoCableMeshObject.loads_conduit`.
* Added `compas_fofin.scene.RhinoCableMeshObject.forces_conduit`.
* Added `compas_fofin.datastructures.CableMesh.is_solved`.
* Added automatic recalculation of equilibrium after modifications if `CableMesh.is_solved = True` at start of command.

### Changed

* Changed "About" to a web-based "Splash" screen.
* Changed `compas_fofin.settings.SETTINGS` to `compas_fofin.settings.Settings` using `dataclasses`.
* Changed `FF_settings` to use the new `Settings` data class.
* Changed visualisation to combination of object drawing and display conduits.

### Removed


## [0.13.0] 2024-08-25

### Added

* Added from RhinoSurface constructor.

### Changed

* Fixed failing redraw on Windows for mesh object select methods.

### Removed


## [0.12.0] 2024-08-24

### Added

* Added density attribute to CableMesh.
* Added selfweight calculation to solver.
* Added MeshGrid constructor for patterns.

### Changed

* Changed loads to be defined by separate components.
* Changed default color of selfweight vectors to white.
* Changed settings dialog to exclude private names.

### Removed


## [0.11.0] 2024-08-23

### Added

### Changed

* Fixed bug in `compas_fofin.rhino.conversions.cylinder_to_cablemesh`.
* Fixed bug in `compas_fofin.rhino.scene.RhinoCableMeshObject.select_vertices` when using loop selection.
* Changed `FF_solve_fd` to use proper vertex indexing.
* Fixed bug in `FF_pattern` to use correct conversion function for cylinders.

### Removed


## [0.10.0] 2024-08-23

### Added

* Added intermediate highlighting of edge loop selections.

### Changed

* Fixed bug in `compas_fofin.session.Session.redo` return clause.
* Fixed bug in redo command.
* Fixed relinking of constraints after serialisation.

### Removed


## [0.9.0] 2024-08-23

### Added

### Changed

### Removed


## [0.8.0] 2024-08-23

### Added

### Changed

### Removed


## [0.7.0] 2023-06-18

### Added

### Changed

* Updated CI/CD setups.

### Removed


## [0.6.0] 2022-11-09

### Added

* Added `compas_fofin.rhino.install.after_rhino_install`.

### Changed

### Removed

* Removed `compas_fofin.rhino.install.main`.


## [0.5.1] 2022-09-23

### Added

### Changed

### Removed


## [0.5.0] 2022-09-23

### Added

### Changed

### Removed


## [0.4.2] 2022-09-23

### Added

### Changed

### Removed


## [0.4.1] 2022-09-23

### Added

### Changed

### Removed


## [0.4.0] 2022-09-23

### Added

### Changed

### Removed


## [0.3.1] 2022-09-22

### Added

### Changed

### Removed


## [0.3.0] 2022-09-21

### Added

### Changed

### Removed


## [0.2.2] 2022-03-24

### Added

### Changed

### Removed


## [0.2.1] 2022-03-23

### Added

### Changed

### Removed


## [0.2.0] 2022-03-22

### Added

### Changed

* Rebased functionality on `compas_ui`.

### Removed

