import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Vector
from compas.scene.descriptors.color import ColorAttribute
from compas_fofin.conduits import EdgesConduit
from compas_fofin.conduits import FacesConduit
from compas_fofin.conduits import MeshConduit
from compas_fofin.conduits import ReactionsConduit
from compas_fofin.conduits import ThickEdgesConduit
from compas_fofin.datastructures import CableMesh
from compas_fofin.session import FoFinSession
from compas_rui.scene import RUIMeshObject


class RhinoCableMeshObject(RUIMeshObject):
    session = FoFinSession()
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
        **kwargs,
    ) -> None:
        super().__init__(disjoint=disjoint, **kwargs)

        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

        self._guids_loads = []
        self._guids_selfweight = []
        self._guids_reactions = []
        self._guids_residuals = []
        self._guids_forces = []

        self._edges_conduit = None
        self._faces_conduit = None
        self._mesh_conduit = None
        self._reactions_conduit = None
        self._loads_conduit = None
        self._forces_conduit = None

    @property
    def settings(self):
        settings = super().settings

        return settings

    # =============================================================================
    # Conduits
    # =============================================================================

    @property
    def edges_conduit(self) -> EdgesConduit:
        if self._edges_conduit is None:
            vertex_index = self.mesh.vertex_index()
            xyz = self.mesh.vertices_attributes("xyz")
            edges = [(vertex_index[u], vertex_index[v]) for u, v in self.mesh.edges()]
            self._edges_conduit = EdgesConduit(
                xyz=xyz,
                edges=edges,
            )
        return self._edges_conduit

    @property
    def faces_conduit(self) -> FacesConduit:
        pass

    @property
    def mesh_conduit(self) -> MeshConduit:
        if self._mesh_conduit is None:
            self._mesh_conduit = MeshConduit(self.mesh, Color(0.8, 0.8, 0.8))
        return self._mesh_conduit

    @property
    def reactions_conduit(self) -> ReactionsConduit:
        if self._reactions_conduit is None:
            self._reactions_conduit = ReactionsConduit(
                self.mesh,
                color=self.reactioncolor,
                scale=self.session.settings.drawing.scale_reactions,
                tol=self.session.settings.drawing.tol_reactions,
            )
        return self._reactions_conduit

    @property
    def loads_conduit(self):
        pass

    @property
    def forces_conduit(self):
        if self._forces_conduit is None:
            vertex_index = self.mesh.vertex_index()
            self._forces_conduit = ThickEdgesConduit(
                xyz=self.mesh.vertices_attributes("xyz"),
                edges=[(vertex_index[u], vertex_index[v]) for u, v in self.mesh.edges()],
                forces=self.mesh.edges_attribute(name="_f"),
            )
        return self._forces_conduit

    # =============================================================================
    # Draw
    # =============================================================================

    def draw(self):
        super().draw()

        if self.session.settings.drawing.show_reactions:
            self.draw_reactions()
        if self.session.settings.drawing.show_residuals:
            self.draw_residuals()
        if self.session.settings.drawing.show_loads:
            self.draw_loads()
        if self.session.settings.drawing.show_selfweight:
            self.draw_selfweight()
        if self.session.settings.drawing.show_forces:
            self.draw_forces()

        return self.guids

    def draw_vertices(self):
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

        scale = self.session.settings.drawing.scale_loads
        tol = self.session.settings.drawing.tol_loads

        for vertex in self.mesh.vertices_where(is_support=False):
            load = self.mesh.vertex_attributes(vertex, ["px", "py", "pz"])

            if load is not None:
                vector = Vector(*load) * scale

                if vector.length > tol:
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

        self._guids_loads = guids
        self._guids += guids
        return guids

    def draw_selfweight(self):
        guids = []

        scale = self.session.settings.drawing.scale_loads
        tol = self.session.settings.drawing.tol_loads

        for vertex in self.mesh.vertices_where(is_support=False):
            thickness = self.mesh.vertex_attribute(vertex, "thickness")

            if thickness:
                area = self.mesh.vertex_area(vertex)
                weight = area * thickness
                point = self.mesh.vertex_point(vertex)
                vector = Vector(0, 0, -weight * scale)

                if vector.length > tol:
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

        self._guids_selfweight = guids
        self._guids += guids
        return guids

    def draw_reactions(self):
        guids = []

        scale = self.session.settings.drawing.scale_reactions
        tol = self.session.settings.drawing.tol_reactions

        for vertex in self.mesh.vertices_where(is_support=True):
            residual = self.mesh.vertex_attribute(vertex, "_residual")

            if residual is not None:
                vector = Vector(*residual) * -scale

                if vector.length > tol:
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

        self._guids_reactions = guids
        self._guids += guids
        return guids

    def draw_residuals(self):
        guids = []

        scale = self.session.settings.drawing.scale_residuals
        tol = self.session.settings.drawing.tol_residuals

        for vertex in self.mesh.vertices_where(is_support=False):
            residual = self.mesh.vertex_attribute(vertex, "_residual")

            if residual is not None:
                vector = Vector(*residual) * scale

                if vector.length > tol:
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

        self._guids_residuals = guids
        self._guids += guids
        return guids

    def draw_forces(self):
        guids = []

        scale = self.session.settings.drawing.scale_forces
        tol = self.session.settings.drawing.tol_forces

        for edge in self.mesh.edges():
            force = self.mesh.edge_attribute(edge, "_f")

            if force != 0:
                line = self.mesh.edge_line(edge)
                radius = abs(force) * scale

                if radius > tol:
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

        self._guids_forces = guids
        self._guids += guids
        return guids

    # =============================================================================
    # Display
    # =============================================================================

    def display_edges_conduit(self, thickness: int = None):
        self.clear_edges_conduit()
        if thickness is not None:
            self.edges_conduit.thickness = thickness
        self.edges_conduit.enable()

    def display_faces_conduit(self):
        self.clear_faces_conduit()
        self.faces_conduit.enable()

    def display_mesh_conduit(self, color: Color = None):
        self.clear_mesh_conduit()
        if color is not None:
            self.mesh_conduit.color = color
        self.mesh_conduit.enable()

    def display_reactions_conduit(self, scale=None, tol=None):
        self.clear_reactions_conduit()
        if scale is not None:
            self.reactions_conduit.scale = scale
        if tol is not None:
            self.reactions_conduit.tol = tol
        self.reactions_conduit.enable()

    def display_forces_conduit(self, tmax: int = None):
        self.clear_forces_conduit()
        if tmax is not None:
            self.forces_conduit.tmax = tmax
        self.forces_conduit.enable()

    # =============================================================================
    # Clear
    # =============================================================================

    def clear(self):
        super().clear()
        self.clear_loads()
        self.clear_selfweight()
        self.clear_reactions()
        self.clear_residuals()
        self.clear_forces()

    def clear_loads(self):
        compas_rhino.objects.delete_objects(self._guids_loads, purge=True)
        self._guids_loads = []

    def clear_selfweight(self):
        compas_rhino.objects.delete_objects(self._guids_selfweight, purge=True)
        self._guids_selfweight = []

    def clear_reactions(self):
        compas_rhino.objects.delete_objects(self._guids_reactions, purge=True)
        self._guids_reactions = []

    def clear_residuals(self):
        compas_rhino.objects.delete_objects(self._guids_residuals, purge=True)
        self._guids_residuals = []

    def clear_forces(self):
        compas_rhino.objects.delete_objects(self._guids_forces, purge=True)
        self._guids_forces = []

    def clear_conduits(self):
        self.clear_edges_conduit()
        self.clear_faces_conduit()
        self.clear_mesh_conduit()
        self.clear_reactions_conduit()
        self.clear_forces_conduit()

    def clear_edges_conduit(self):
        try:
            self.edges_conduit.disable()
        except:  # noqa: E722
            pass
        finally:
            del self._edges_conduit
            self._edges_conduit = None

    def clear_faces_conduit(self):
        try:
            self.faces_conduit.disable()
        except:  # noqa: E722
            pass
        finally:
            del self._faces_conduit
            self._faces_conduit = None

    def clear_mesh_conduit(self):
        try:
            self.mesh_conduit.disable()
        except:  # noqa: E722
            pass
        finally:
            del self._mesh_conduit
            self._mesh_conduit = None

    def clear_reactions_conduit(self):
        try:
            self.reactions_conduit.disable()
        except:  # noqa: E722
            pass
        finally:
            del self._reactions_conduit
            self._reactions_conduit = None

    def clear_forces_conduit(self):
        try:
            self.forces_conduit.disable()
        except:  # noqa: E722
            pass
        finally:
            del self._forces_conduit
            self._forces_conduit = None

    # =============================================================================
    # Redraw
    # =============================================================================

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_vertices(self):
        rs.EnableRedraw(False)
        self.clear_vertices()
        self.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_edges(self):
        rs.EnableRedraw(False)
        self.clear_edges()
        self.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_faces(self):
        rs.EnableRedraw(False)
        self.clear_faces()
        self.draw_faces()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_loads(self):
        rs.EnableRedraw(False)
        self.clear_loads()
        self.draw_loads()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_selfweight(self):
        rs.EnableRedraw(False)
        self.clear_selfweight()
        self.draw_selfweight()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_reactions(self):
        rs.EnableRedraw(False)
        self.clear_reactions()
        self.draw_reactions()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_residuals(self):
        rs.EnableRedraw(False)
        self.clear_residuals()
        self.draw_residuals()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_forces(self):
        rs.EnableRedraw(False)
        self.clear_forces()
        self.draw_forces()
        rs.EnableRedraw(True)
        rs.Redraw()
