import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Vector
from compas.scene.descriptors.color import ColorAttribute
from compas_fofin.datastructures import CableMesh
from compas_rui.scene import RUIMeshObject


class RhinoCableMeshObject(RUIMeshObject):
    mesh: CableMesh

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    constraintcolor = ColorAttribute(default=Color.cyan())
    residualcolor = ColorAttribute(default=Color.cyan())
    reactioncolor = ColorAttribute(default=Color.green())
    loadcolor = ColorAttribute(default=Color.green().darkened(50))
    selfweightcolor = ColorAttribute(default=Color.white())
    compressioncolor = ColorAttribute(default=Color.blue())
    tensioncolor = ColorAttribute(default=Color.red())

    def __init__(
        self,
        disjoint=True,
        loadgroup=None,
        selfweightgroup=None,
        forcegroup=None,
        reactiongroup=None,
        residualgroup=None,
        show_supports=True,
        show_free=False,
        show_forces=False,
        show_residuals=False,
        show_reactions=False,
        show_loads=False,
        show_selfweight=False,
        scale_loads=1.0,
        scale_forces=1.0,
        scale_residuals=1.0,
        scale_selfweight=1.0,
        tol_vectors=1e-3,
        tol_pipes=1e-3,
        **kwargs,
    ) -> None:
        super().__init__(disjoint=disjoint, **kwargs)

        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

        self.show_supports = show_supports
        self.show_free = show_free
        self.show_forces = show_forces
        self.show_residuals = show_residuals
        self.show_reactions = show_reactions
        self.show_loads = show_loads
        self.show_selfweight = show_selfweight

        self.scale_loads = scale_loads
        self.scale_forces = scale_forces
        self.scale_residuals = scale_residuals
        self.scale_selfweight = scale_selfweight

        self.tol_vectors = tol_vectors
        self.tol_pipes = tol_pipes

        self.is_valid = False

    @property
    def settings(self):
        settings = super().settings

        settings["show_supports"] = self.show_supports
        settings["show_free"] = self.show_free
        settings["show_forces"] = self.show_forces
        settings["show_residuals"] = self.show_residuals
        settings["show_reactions"] = self.show_reactions
        settings["show_loads"] = self.show_loads
        settings["show_selfweight"] = self.show_selfweight

        settings["scale_loads"] = self.scale_loads
        settings["scale_forces"] = self.scale_forces
        settings["scale_residuals"] = self.scale_residuals
        settings["scale_selfweight"] = self.scale_selfweight

        settings["tol_vectors"] = self.tol_vectors
        settings["tol_pipes"] = self.tol_pipes

        settings["freecolor"] = self.freecolor
        settings["anchorcolor"] = self.anchorcolor
        settings["constraintcolor"] = self.constraintcolor
        settings["residualcolor"] = self.residualcolor
        settings["reactioncolor"] = self.reactioncolor
        settings["loadcolor"] = self.loadcolor
        settings["selfweightcolor"] = self.selfweightcolor
        settings["compressioncolor"] = self.compressioncolor
        settings["tensioncolor"] = self.tensioncolor

        return settings

    def draw(self):
        """Draw the mesh or its components in Rhino.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                if not self.mesh.vertex_attribute(vertex, "constraint"):
                    self.vertexcolor[vertex] = self.anchorcolor
                else:
                    self.vertexcolor[vertex] = self.constraintcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        super().draw()

        if self.show_reactions:
            self.draw_reactions()
        if self.show_residuals:
            self.draw_residuals()
        if self.show_loads:
            self.draw_loads()
        if self.show_selfweight:
            self.draw_selfweight()
        if self.show_forces:
            self.draw_forces()

        return self.guids

    def draw_vertices(self):
        vertices = []

        if self.show_free:
            vertices += list(self.mesh.vertices_where(is_support=False))
        if self.show_supports:
            vertices += list(self.mesh.vertices_where(is_support=True))
        if vertices:
            self.show_vertices = vertices

        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                if not self.mesh.vertex_attribute(vertex, "constraint"):
                    self.vertexcolor[vertex] = self.anchorcolor
                else:
                    self.vertexcolor[vertex] = self.constraintcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()

    def draw_loads(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_support=False):
            load = self.mesh.vertex_attributes(vertex, ["px", "py", "pz"])

            if load is not None:
                vector = Vector(*load) * self.scale_loads
                if vector.length > self.tol_vectors:
                    name = "{}.vertex.{}.load".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.loadcolor, arrow="end")
                    point = self.mesh.vertex_point(vertex)
                    line = Line.from_point_and_vector(point, vector)
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.loadgroup:
                self.add_to_group(self.loadgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_selfweight(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_support=False):
            thickness = self.mesh.vertex_attribute(vertex, "thickness")

            if thickness:
                area = self.mesh.vertex_area(vertex)
                weight = area * thickness
                point = self.mesh.vertex_point(vertex)
                vector = Vector(0, 0, -weight * self.scale_selfweight)
                if vector.length > self.tol_vectors:
                    line = Line.from_point_and_vector(point, vector)
                    name = "{}.vertex.{}.selfweight".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.selfweightcolor, arrow="end")
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.selfweightgroup:
                self.add_to_group(self.selfweightgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_forces(self):
        guids = []

        for edge in self.mesh.edges():
            force = self.mesh.edge_attribute(edge, "_f")

            if force != 0:
                line = self.mesh.edge_line(edge)
                radius = abs(force) * self.scale_forces
                if radius > self.tol_pipes:
                    pipe = Cylinder.from_line_and_radius(line, radius)
                    name = "{}.edge.{}.force".format(self.mesh.name, edge)
                    attr = self.compile_attributes(name=name, color=self.compressioncolor if force < 0 else self.tensioncolor)
                    guid = sc.doc.Objects.AddBrep(compas_rhino.conversions.cylinder_to_rhino_brep(pipe), attr)
                    guids.append(guid)

        if guids:
            if self.forcegroup:
                self.add_to_group(self.forcegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_reactions(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_support=True):
            residual = self.mesh.vertex_attribute(vertex, "_residual")

            if residual is not None:
                vector = Vector(*residual) * -self.scale_residuals
                if vector.length > self.tol_vectors:
                    name = "{}.vertex.{}.reaction".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.reactioncolor, arrow="end")
                    point = self.mesh.vertex_point(vertex)
                    line = Line.from_point_and_vector(point, vector)
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.reactiongroup:
                self.add_to_group(self.reactiongroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_residuals(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_support=False):
            residual = self.mesh.vertex_attribute(vertex, "_residual")

            if residual is not None:
                vector = Vector(*residual) * self.scale_residuals
                if vector.length > self.tol_vectors:
                    name = "{}.vertex.{}.residual".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.residualcolor, arrow="end")
                    point = self.mesh.vertex_point(vertex)
                    line = Line.from_point_and_vector(point, vector)
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.residualgroup:
                self.add_to_group(self.residualgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids
