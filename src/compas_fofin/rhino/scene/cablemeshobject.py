import ast

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas_fofin.datastructures import CableMesh
from compas_fofin.scene import CableMeshObject
from compas_rhino.scene import RhinoMeshObject


class RhinoCableMeshObject(RhinoMeshObject, CableMeshObject):
    mesh: CableMesh

    def __init__(
        self,
        disjoint=True,
        loadgroup=None,
        selfweightgroup=None,
        forcegroup=None,
        reactiongroup=None,
        residualgroup=None,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)
        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Constraints
    # =============================================================================
    # =============================================================================
    # =============================================================================

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Select
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def select_vertices(self, show_anchors=True, show_free=True):
        option = rs.GetString(message="Select Vertices", strings=["Degree", "EdgeLoop", "Manual"])
        if not option:
            return

        if option == "Degree":
            D = rs.GetInteger(message="Vertex Degree", number=2, minimum=1)
            if not D:
                return

            return self.mesh.vertices_where(vertex_degree=D)

        if option == "EdgeLoop":
            self.show_edges = True
            self.clear_edges()
            self.draw_edges()

            rs.EnableRedraw(True)
            rs.Redraw()

            guids = compas_rhino.objects.select_lines(message="Select Edges")
            if not guids:
                return

            edges = [self._guid_edge.get(guid) for guid in guids]

            edge_guid = {edge: guid for guid, edge in self._guid_edge.items()}
            edge_guid.update({(v, u): guid for (u, v), guid in edge_guid.items()})

            selected = []
            vertices = []
            for edge in edges:
                loop = self.mesh.edge_loop(edge)

                for u, v in loop:
                    selected.append(edge_guid[u, v])

                    vertices.append(u)
                    vertices.append(v)

            rs.UnselectAllObjects()
            rs.SelectObjects(selected)

            return list(set(vertices))

        if option == "Manual":
            self.show_anchors = show_anchors
            self.show_free = show_free
            self.clear_vertices()
            self.draw_vertices()

            rs.EnableRedraw(True)
            rs.Redraw()

            guids = compas_rhino.objects.select_points(message="Select Vertices")
            if not guids:
                return

            return [self._guid_vertex.get(guid) for guid in guids]

    def select_edges(self):
        option = rs.GetString(message="Select Edges", strings=["EdgeLoop", "Manual", "All"])
        if not option:
            return

        if option == "EdgeLoop":
            self.show_edges = True
            self.clear_edges()
            self.draw_edges()

            rs.EnableRedraw(True)
            rs.Redraw()

            guids = compas_rhino.objects.select_lines(message="Select Edges")
            if not guids:
                return

            edges = []
            for guid in guids:
                edge = self._guid_edge[guid]
                for edge in self.mesh.edge_loop(edge):
                    edges.append(edge)

            edge_guid = {edge: guid for guid, edge in self._guid_edge.items()}
            edge_guid.update({(v, u): guid for (u, v), guid in edge_guid.items()})

            rs.UnselectAllObjects()
            rs.SelectObjects([edge_guid[edge] for edge in edges])

            return edges

        if option == "Manual":
            self.show_edges = True
            self.clear_edges()
            self.draw_edges()

            rs.EnableRedraw(True)
            rs.Redraw()

            guids = compas_rhino.objects.select_lines(message="Select Edges")
            if not guids:
                return

            return [self._guid_edge.get(guid) for guid in guids]

        if option == "All":
            return list(self.mesh.edges())

    def select_faces(self, redraw=True):
        if redraw:
            self.clear_faces()
            self.draw_faces()

            rs.EnableRedraw(True)
            rs.Redraw()

        guids = compas_rhino.objects.select_meshes(message="Select Faces")
        if not guids:
            return

        return [self._guid_face.get(guid) for guid in guids]

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Draw
    # =============================================================================
    # =============================================================================
    # =============================================================================

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
            if self.mesh.vertex_attribute(vertex, "is_anchor"):
                if not self.mesh.vertex_attribute(vertex, "constraint"):
                    self.vertexcolor[vertex] = self.anchorcolor
                else:
                    self.vertexcolor[vertex] = self.constraintcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        super(RhinoCableMeshObject, self).draw()

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
            vertices += list(self.mesh.vertices_where(is_anchor=False))
        if self.show_anchors:
            vertices += list(self.mesh.vertices_where(is_anchor=True))
        if vertices:
            self.show_vertices = vertices

        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_anchor"):
                if not self.mesh.vertex_attribute(vertex, "constraint"):
                    self.vertexcolor[vertex] = self.anchorcolor
                else:
                    self.vertexcolor[vertex] = self.constraintcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()

    def draw_loads(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_anchor=False):
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

        for vertex in self.mesh.vertices_where(is_anchor=False):
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

        for vertex in self.mesh.vertices_where(is_anchor=True):
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

        for vertex in self.mesh.vertices_where(is_anchor=False):
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

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Modify
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def update_attributes(self):
        # type: () -> bool

        mesh = self.mesh  # type: CableMesh

        names = sorted(mesh.attributes.keys())
        values = [str(mesh.attributes[name]) for name in names]
        values = rs.PropertyListBox(names, values, message="General Attributes", title="Update Mesh")
        if values:
            for name, value in zip(names, values):
                try:
                    mesh.attributes[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    mesh.attributes[name] = value
            return True
        return False

    def update_vertex_attributes(self, vertices, names=None):
        # type: (list[int], list[str] | None) -> bool

        mesh = self.mesh  # type: CableMesh

        names = names or mesh.default_vertex_attributes.keys()
        names = sorted(
            [
                name
                for name in names
                if not name.startswith("_")
                and name
                not in [
                    "constraint",
                ]
            ]
        )
        values = mesh.vertex_attributes(vertices[0], names)
        if len(vertices) > 1:
            for i, name in enumerate(names):
                for vertex in vertices[1:]:
                    if values[i] != mesh.vertex_attribute(vertex, name):
                        values[i] = "-"
                        break
        values = map(str, values)
        values = rs.PropertyListBox(names, values, message="Vertex Attributes", title="Update Mesh")
        if values:
            for name, value in zip(names, values):
                if value == "-":
                    continue
                for vertex in vertices:
                    try:
                        mesh.vertex_attribute(vertex, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        mesh.vertex_attribute(vertex, name, value)
            return True
        return False

    def update_face_attributes(self, faces, names=None):
        # type: (list[int], list[str] | None) -> bool

        mesh = self.mesh  # type: CableMesh

        names = names or mesh.default_face_attributes.keys()
        names = sorted([name for name in names if not name.startswith("_")])
        values = mesh.face_attributes(faces[0], names)
        if len(faces) > 1:
            for i, name in enumerate(names):
                for face in faces[1:]:
                    if values[i] != mesh.face_attribute(face, name):
                        values[i] = "-"
                        break
        values = map(str, values)
        values = rs.PropertyListBox(names, values, message="Face Attributes", title="Update Mesh")
        if values:
            for name, value in zip(names, values):
                if value == "-":
                    continue
                for face in faces:
                    try:
                        mesh.face_attribute(face, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        mesh.face_attribute(face, name, value)
            return True
        return False

    def update_edge_attributes(self, edges, names=None):
        # type: (list[tuple[int, int]], list[str] | None) -> bool

        mesh = self.mesh  # type: CableMesh

        names = names or mesh.default_edge_attributes.keys()
        names = sorted([name for name in names if not name.startswith("_")])
        edge = edges[0]
        values = mesh.edge_attributes(edge, names)
        if len(edges) > 1:
            for i, name in enumerate(names):
                for edge in edges[1:]:
                    if values[i] != mesh.edge_attribute(edge, name):
                        values[i] = "-"
                        break
        values = map(str, values)
        values = rs.PropertyListBox(names, values, message="CableMesh Edge Attributes", title="FormFinder")
        if values:
            for name, value in zip(names, values):
                if value == "-":
                    continue
                for edge in edges:
                    try:
                        value = ast.literal_eval(value)
                    except (SyntaxError, ValueError, TypeError):
                        pass
                    mesh.edge_attribute(edge, name, value)
            return True
        return False

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Move
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def move(self):
        # type: () -> bool

        mesh = self.mesh  # type: CableMesh

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

        vertex_p0 = {v: Rhino.Geometry.Point3d(*mesh.vertex_coordinates(v)) for v in mesh.vertices()}
        vertex_p1 = {v: Rhino.Geometry.Point3d(*mesh.vertex_coordinates(v)) for v in mesh.vertices()}

        edges = list(mesh.edges())

        def OnDynamicDraw(sender, e):
            current = e.CurrentPoint
            vector = current - start
            for vertex in vertex_p1:
                vertex_p1[vertex] = vertex_p0[vertex] + vector
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for _, attr in mesh.vertices(True):
            attr["x"] += vector[0]
            attr["y"] += vector[1]
            attr["z"] += vector[2]

        return True

    def move_vertex(self, vertex, constraint=None, allow_off=True):
        # type: (int, Rhino.Geometry, bool) -> bool

        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        mesh = self.mesh  # type: CableMesh

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [mesh.vertex_coordinates(nbr) for nbr in mesh.vertex_neighbors(vertex)]
        nbrs = [Rhino.Geometry.Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        mesh.vertex_attributes(vertex, "xyz", list(gp.Point()))
        return True

    def move_vertices(self, vertices):
        # type: (list[int]) -> bool

        def OnDynamicDraw(sender, e):
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                e.Display.DrawDottedLine(a, b, color)
            for a, b in connectors:
                a = a + vector
                e.Display.DrawDottedLine(a, b, color)

        mesh = self.mesh  # type: CableMesh

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = mesh.vertex_coordinates(vertex)
            nbrs = mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = mesh.vertex_coordinates(nbr)
                line = [Rhino.Geometry.Point3d(*a), Rhino.Geometry.Point3d(*b)]
                if nbr in vertices:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for vertex in vertices:
            point = Point(*mesh.vertex_attributes(vertex, "xyz"))
            mesh.vertex_attributes(vertex, "xyz", point + vector)
        return True

    def move_vertices_direction(self, vertices, direction):
        # type: (list[int], str) -> bool

        def OnDynamicDraw(sender, e):
            draw = e.Display.DrawDottedLine
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                draw(a, b, color)
            for a, b in connectors:
                a = a + vector
                draw(a, b, color)

        mesh = self.mesh  # type: CableMesh

        direction = direction.lower()
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = Rhino.Geometry.Point3d(*mesh.vertex_coordinates(vertex))
            nbrs = mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = Rhino.Geometry.Point3d(*mesh.vertex_coordinates(nbr))
                if nbr in vertices:
                    lines.append((a, b))
                else:
                    connectors.append((a, b))

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        if direction == "x":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "y":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 1, 0))
        elif direction == "z":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "xy":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "yz":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "zx":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 1, 0))

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw

        if direction in ("x", "y", "z"):
            gp.Constrain(geometry)
        else:
            gp.Constrain(geometry, False)

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for vertex in vertices:
            point = mesh.vertex_point(vertex)
            mesh.vertex_attributes(vertex, "xyz", point + vector)

        return True
