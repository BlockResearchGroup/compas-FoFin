import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Vector
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import CableMeshObject
from compas_rhino.scene import RhinoMeshObject


class RhinoCableMeshObject(RhinoMeshObject, CableMeshObject):

    mesh: CableMesh

    def __init__(
        self,
        loadgroup=None,
        selfweightgroup=None,
        forcegroup=None,
        reactiongroup=None,
        residualgroup=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

    def select_vertices(self, redraw=True):
        if redraw:
            self.clear_vertices()
            self.draw_vertices()

        guids = compas_rhino.objects.select_points(message="Select Vertices")
        if not guids:
            return

        return [self._guid_vertex.get(guid) for guid in guids]

    def select_edges(self, redraw=True):
        if redraw:
            self.clear_edges()
            self.draw_edges()

        guids = compas_rhino.objects.select_lines(message="Select Edges")
        if not guids:
            return

        return [self._guid_edge.get(guid) for guid in guids]

    def select_faces(self, redraw=True):
        if redraw:
            self.clear_faces()
            self.draw_faces()

        guids = compas_rhino.objects.select_meshes(message="Select Faces")
        if not guids:
            return

        return [self._guid_face.get(guid) for guid in guids]

    def draw_vertices(self):
        vertices = []

        if self.show_free:
            vertices += list(self.mesh.vertices_where(is_anchor=False))
        if self.show_anchors:
            vertices += list(self.mesh.vertices_where(is_anchor=True))
        if vertices:
            self.show_vertices = vertices

        for vertex in self.mesh.vertices_where(is_anchor=True):
            if not self.mesh.vertex_attribute(vertex, "constraint"):
                self.vertexcolor[vertex] = self.anchorcolor
            else:
                self.vertexcolor[vertex] = self.constraintcolor

        return super().draw_vertices()

    def draw_loads(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_anchor=False):
            load = self.mesh.vertex_load(vertex)

            if load is not None:
                name = "{}.vertex.{}.load".format(self.mesh.name, vertex)
                attr = self.compile_attributes(name=name, color=self.loadcolor, arrow="end")
                point = self.mesh.vertex_point(vertex)
                line = Line.from_point_and_vector(point, load * self.scale_loads)
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

        for vertex in self.mesh.vertices_where(is_anchor=False):
            thickness = self.mesh.vertex_attribute(vertex, "t")

            if thickness:
                area = self.mesh.vertex_area(vertex)
                weight = area * thickness
                point = self.mesh.vertex_point(vertex)
                vector = Vector(0, 0, weight * self.scale_selfweight)
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
                pipe = Cylinder.from_line_and_radius(line, radius)
                name = "{}.edge.{}.force".format(self.mesh.name, edge)
                attr = self.compile_attributes(name=name, color=self.compressioncolor if force < 0 else self.tensioncolor)
                guid = sc.doc.Objects.AddCylinder(compas_rhino.conversions.cylinder_to_rhino(pipe), attr)
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

        for vertex in self.mesh.vertices_where(is_anchor=True):
            residual = self.mesh.vertex_residual(vertex)

            if residual is not None:
                name = "{}.vertex.{}.reaction".format(self.mesh.name, vertex)
                attr = self.compile_attributes(name=name, color=self.reactioncolor, arrow="end")
                point = self.mesh.vertex_point(vertex)
                line = Line.from_point_and_vector(point, residual * -self.scale_residuals)
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

        for vertex in self.mesh.vertices_where(is_anchor=False):
            residual = self.mesh.vertex_residual(vertex)

            if residual is not None:
                name = "{}.vertex.{}.residual".format(self.mesh.name, vertex)
                attr = self.compile_attributes(name=name, color=self.residualcolor, arrow="end")
                point = self.mesh.vertex_point(vertex)
                line = Line.from_point_and_vector(point, residual * self.scale_residuals)
                guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                guids.append(guid)

        if guids:
            if self.residualgroup:
                self.add_to_group(self.residualgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids
