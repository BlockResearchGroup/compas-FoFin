from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.colors import Color
from compas.colors import ColorMap
from compas.geometry import Line
from compas.geometry import NurbsCurve
from compas.geometry import NurbsSurface

from compas_ui.rhino.objects import RhinoMeshObject

from compas_fofin.objects import CableMeshObject
from compas_fofin.rhino.conduits import ReactionConduit
from compas_fofin.rhino.conduits import LoadConduit
from compas_fofin.rhino.conduits import PipeConduit


RED = ColorMap.from_two_colors(Color.white(), Color.red())
BLUE = ColorMap.from_two_colors(Color.white(), Color.blue())


class RhinoCableMeshObject(CableMeshObject, RhinoMeshObject):
    """Scene object for FF CableMeshes.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoCableMeshObject, self).__init__(*args, **kwargs)
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_pipes_f = None
        self._conduit_pipes_q = None

    def __getstate__(self):
        dictcopy = super(RhinoCableMeshObject, self).__getstate__()
        dictcopy['_conduit_reactions'] = None
        dictcopy['_conduit_loads'] = None
        dictcopy['_conduit_pipes_f'] = None
        dictcopy['_conduit_pipes_q'] = None
        return dictcopy

    @property
    def group_free(self):
        if not self._group_free:
            group = "{}::vertices::free".format(self.layer)
            self._group_free = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_free

    @property
    def group_fixed(self):
        if not self._group_fixed:
            group = "{}::vertices::fixed".format(self.layer)
            self._group_fixed = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_fixed

    @property
    def group_anchors(self):
        if not self._group_anchors:
            group = "{}::vertices::anchors".format(self.layer)
            self._group_anchors = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_anchors

    @property
    def group_edges(self):
        if not self._group_edges:
            group = "{}::edges".format(self.layer)
            self._group_edges = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_edges

    @property
    def group_faces(self):
        if not self._group_faces:
            group = "{}::faces".format(self.layer)
            self._group_faces = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_faces

    @property
    def conduit_reactions(self):
        if not self._conduit_reactions:
            self._conduit_reactions = ReactionConduit(
                self.mesh,
                color=self.settings['color.reactions'].rgb255,
                scale=self.settings['scale.externalforces'],
                tol=self.settings['tol.externalforces']
            )
        return self._conduit_reactions

    @property
    def conduit_loads(self):
        if not self._conduit_loads:
            self._conduit_loads = LoadConduit(
                self.mesh,
                color=self.settings['color.loads'].rgb255,
                scale=self.settings['scale.externalforces'],
                tol=self.settings['tol.externalforces']
            )
        return self._conduit_loads

    @property
    def conduit_pipes_f(self):
        if not self._conduit_pipes_f:
            self._conduit_pipes_f = PipeConduit(xyz={}, edges=[], values={}, color={})
        return self._conduit_pipes_f

    @property
    def conduit_pipes_q(self):
        if not self._conduit_pipes_q:
            self._conduit_pipes_q = PipeConduit(xyz={}, edges=[], values={}, color={})
        return self._conduit_pipes_q

    def clear_conduits(self):
        try:
            self.conduit_reactions.disable()
        except Exception:
            pass
        finally:
            del self._conduit_reactions
            self._conduit_reactions = None

        try:
            self.conduit_loads.disable()
        except Exception:
            pass
        finally:
            del self._conduit_loads
            self._conduit_loads = None

        try:
            self.conduit_pipes_f.disable()
        except Exception:
            pass
        finally:
            del self._conduit_pipes_f
            self._conduit_pipes_f = None

        try:
            self.conduit_pipes_q.disable()
        except Exception:
            pass
        finally:
            del self._conduit_pipes_q
            self._conduit_pipes_q = None

    def clear(self):
        super(CableMeshObject, self).clear()
        self.clear_conduits()

    def draw(self):
        layer = self.layer

        self.artist.layer = layer
        self.artist.clear_layer()

        self.clear()
        if not self.visible:
            return

        self.artist.vertex_xyz = self.vertex_xyz

        self._draw_vertices()
        self._draw_edges()
        self._draw_faces()
        self._draw_reaction_overlays()
        self._draw_load_overlays()
        self._draw_force_overlays()
        self._draw_q_overlays()

    # ======================================================================
    # Vertices
    # --------
    # Draw the vertices and add them to the vertex group.
    # Free vertices and anchored vertices are drawn separately.
    # ======================================================================

    def _draw_vertices(self):

        free = list(self.mesh.vertices_where(is_anchor=False))
        fixed = list(self.mesh.vertices_where(is_fixed=True))
        anchored = list(self.mesh.vertices_where(is_anchor=True))
        constrained = list(self.mesh.vertices_where_predicate(lambda key, attr: attr['constraint'] is not None))

        color_free = self.settings['color.vertices'] if self.is_valid else self.settings['color.invalid']
        color_fixed = self.settings['color.vertices:is_fixed']
        color_anchored = self.settings['color.vertices:is_anchor']
        color_constrained = self.settings['color.vertices:is_constrained']

        vertex_color = {vertex: color_free for vertex in free}
        vertex_color.update({vertex: color_fixed for vertex in fixed})
        vertex_color.update({vertex: color_anchored for vertex in anchored})
        vertex_color.update({vertex: color_constrained for vertex in constrained})

        guids_free = []
        guids_anchor = []

        if free:
            guids_free = self.artist.draw_vertices(vertices=free, color=vertex_color)
        if anchored:
            guids_anchor = self.artist.draw_vertices(vertices=anchored, color=vertex_color)

        compas_rhino.rs.AddObjectsToGroup(guids_free, self.group_free)
        compas_rhino.rs.AddObjectsToGroup(guids_anchor, self.group_anchors)

        if self.settings['show.vertices:is_anchor']:
            compas_rhino.rs.ShowGroup(self.group_anchors)
        else:
            compas_rhino.rs.HideGroup(self.group_anchors)

        if self.settings['show.vertices:free']:
            compas_rhino.rs.ShowGroup(self.group_free)
        else:
            compas_rhino.rs.HideGroup(self.group_free)

        guids = guids_free + guids_anchor
        vertices = free + anchored

        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

        if self.settings['show.constraints']:
            if constrained:
                text = {}
                for vertex in constrained:
                    constraint = self.mesh.vertex_attribute(vertex, 'constraint')
                    if isinstance(constraint.geometry, Line):
                        text[vertex] = 'L'
                    elif isinstance(constraint.geometry, NurbsCurve):
                        text[vertex] = 'C'
                    elif isinstance(constraint.geometry, NurbsSurface):
                        text[vertex] = 'S'
                self.guids += self.artist.draw_vertexlabels(text)

    # ======================================================================
    # Edges
    # -----
    # Draw the edges and add them to the edge group.
    # ======================================================================

    def _draw_edges(self):

        edges = list(self.mesh.edges_where(_is_edge=True))

        if not self.is_valid:
            edge_color = {edge: self.settings['color.invalid'] for edge in edges}
        else:
            edge_q = {edge: self.mesh.edge_attribute(edge, 'q') for edge in edges}
            edge_color = {}
            for edge in edges:
                color = self.settings['color.edges:compression'] if edge_q[edge] < 0.0 else self.settings['color.edges:tension']
                edge_color[edge] = color

        guids = self.artist.draw_edges(edges, edge_color)

        compas_rhino.rs.AddObjectsToGroup(guids, self.group_edges)

        if self.settings['show.edges']:
            compas_rhino.rs.ShowGroup(self.group_edges)
        else:
            compas_rhino.rs.HideGroup(self.group_edges)

        self.guids += guids
        self.guid_edge = zip(guids, edges)

    # ======================================================================
    # Faces
    # -----
    # Draw the faces and add them to the face group.
    # ======================================================================

    def _draw_faces(self):

        if self.settings['show.faces:all']:
            faces = list(self.mesh.faces())
        else:
            faces = list(self.mesh.faces_where(is_loaded=True))

        if faces:
            color = {face: self.settings['color.faces'] for face in faces}
            guids = self.artist.draw_faces(faces, color)

            compas_rhino.rs.AddObjectsToGroup(guids, self.group_faces)

            if self.settings['show.faces']:
                compas_rhino.rs.ShowGroup(self.group_faces)
            else:
                compas_rhino.rs.HideGroup(self.group_faces)

            self.guids += guids
            self.guid_face = zip(guids, faces)

    # ======================================================================
    # Overlays
    # --------
    # Color overlays for various display modes.
    # ======================================================================

    def _draw_reaction_overlays(self):

        if self.is_valid and self.settings['show.reactions']:

            self.conduit_reactions.color = self.settings['color.reactions'].rgb255
            self.conduit_reactions.scale = self.settings['scale.externalforces']
            self.conduit_reactions.tol = self.settings['tol.externalforces']
            self.conduit_reactions.enable()
        else:
            if self.conduit_reactions:
                try:
                    self.conduit_reactions.disable()
                except Exception:
                    pass

    def _draw_load_overlays(self):

        if self.settings['show.loads']:
            self.conduit_loads.color = self.settings['color.loads'].rgb255
            self.conduit_loads.scale = self.settings['scale.externalforces']
            self.conduit_loads.tol = self.settings['tol.externalforces']
            self.conduit_loads.enable()
        else:
            if self.conduit_loads:
                try:
                    self.conduit_loads.disable()
                except Exception:
                    pass

    def _draw_force_overlays(self):

        if self.is_valid and self.settings['show.pipes:forces']:

            xyz = {vertex: self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.vertices()}
            edges = list(self.mesh.edges_where(_is_edge=True))
            edge_color = {edge: self.settings['color.pipes'].rgb255 for edge in edges}
            edge_force = {edge: self.mesh.edge_attribute(edge, '_f') for edge in edges}

            fmin = min(edge_force.values())
            fmax = max(edge_force.values())
            f_range = (fmax - fmin) or 1

            tmin = self.settings['pipe_thickness.min']
            tmax = self.settings['pipe_thickness.max']
            t_range = tmax - tmin

            forces_remapped = {edge: (((force - fmin) * t_range) / f_range) + tmin for edge, force in iter(edge_force.items())}

            if fmin != fmax:
                for edge in edges:
                    force = edge_force[edge]
                    if force >= 0.0:
                        edge_color[edge] = RED(force / fmax).rgb255
                    elif force < 0.0:
                        edge_color[edge] = BLUE(force / fmin).rgb255

            self.conduit_pipes_f.xyz = xyz
            self.conduit_pipes_f.edges = edges
            self.conduit_pipes_f.values = forces_remapped
            self.conduit_pipes_f.color = edge_color
            self.conduit_pipes_f.enable()

        else:
            if self.conduit_pipes_f:
                try:
                    self.conduit_pipes_f.disable()
                except Exception:
                    pass

    def _draw_q_overlays(self):

        if self.settings['_is.valid'] and self.settings['show.pipes:forcedensities']:

            xyz = {vertex: self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.vertices()}
            edges = list(self.mesh.edges_where(_is_edge=True))
            edge_color = {edge: self.settings['color.pipes'].rgb255 for edge in edges}
            edge_q = {edge: self.mesh.edge_attribute(edge, 'q') for edge in edges}

            qmin = min(edge_q.values())
            qmax = max(edge_q.values())
            q_range = (qmax - qmin) or 1

            tmin = self.settings['pipe_thickness.min']
            tmax = self.settings['pipe_thickness.max']
            t_range = tmax - tmin

            q_remapped = {edge: (((q - qmin) * t_range) / q_range) + tmin for edge, q in iter(edge_q.items())}

            if qmin != qmax:
                for edge in edges:
                    q = edge_q[edge]
                    if q >= 0.0:
                        edge_color[edge] = RED(q / qmax).rgb255
                    elif q < 0.0:
                        edge_color[edge] = BLUE(q / qmin).rgb255

            self.conduit_pipes_q.xyz = xyz
            self.conduit_pipes_q.edges = edges
            self.conduit_pipes_q.values = q_remapped
            self.conduit_pipes_q.color = edge_color
            self.conduit_pipes_q.enable()

        else:
            if self.conduit_pipes_q:
                try:
                    self.conduit_pipes_q.disable()
                except Exception:
                    pass

    # ======================================================================
    # Constraints
    # ======================================================================

    def move_vertex_on_constraint(self, vertex):
        pass
