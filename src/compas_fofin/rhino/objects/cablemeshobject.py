from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.colors import Color
from compas.colors import ColorMap

from compas_ui.rhino.objects import RhinoMeshObject

from compas_fofin.objects import CableMeshObject
from compas_fofin.rhino.conduits import ReactionConduit
from compas_fofin.rhino.conduits import LoadConduit
from compas_fofin.rhino.conduits import PipeConduit


RED = ColorMap.from_color(Color.red())
BLUE = ColorMap.from_color(Color.blue())


class RhinoCableMeshObject(CableMeshObject, RhinoMeshObject):
    """Scene object for FF CableMeshes.
    """

    SETTINGS = {
        '_is.valid': False,

        'layer': "FF::CableMesh",

        'show.vertices:is_anchor': True,
        'show.vertices:free': False,
        'show.edges': True,
        'show.faces': False,
        'show.faces:all': False,
        'show.reactions': True,
        'show.loads': True,
        'show.pipes:forcedensities': False,
        'show.pipes:forces': True,

        'color.vertices': Color.white(),
        'color.vertices:is_anchor': Color.red(),
        'color.vertices:is_fixed': Color.blue(),
        'color.vertices:is_constrained': Color.cyan(),
        'color.edges': Color.black(),
        'color.edges:tension': Color.red(),
        'color.edges:compression': Color.blue(),
        'color.faces': Color.white().darkened(25),
        'color.reactions': Color.green().darkened(50),
        'color.loads': Color.green().darkened(75),
        'color.invalid': Color.magenta(),
        'color.pipes': Color.white().darkened(50),

        'scale.externalforces': 1,
        'pipe_thickness.min': 0,
        'pipe_thickness.max': 10,
        'tol.externalforces': 1e-3,
    }

    def __init__(self, *args, **kwargs):
        super(RhinoCableMeshObject, self).__init__(*args, **kwargs)
        self._group_free = None
        self._group_fixed = None
        self._group_anchors = None
        self._group_edges = None
        self._group_faces = None
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_pipes_f = None
        self._conduit_pipes_q = None

    @property
    def layer(self):
        return self.settings.get('layer')

    @layer.setter
    def layer(self, value):
        self.settings['layer'] = value

    @property
    def is_valid(self):
        return self.settings.get('_is.valid')

    @is_valid.setter
    def is_valid(self, value):
        self.settings['_is.valid'] = value

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
        try: self.conduit_reactions.disable()  # noqa : E701
        except Exception: pass  # noqa : E701
        finally: del self._conduit_reactions  # noqa : E701

        try: self.conduit_loads.disable()  # noqa : E701
        except Exception: pass  # noqa : E701
        finally: del self._conduit_loads  # noqa : E701

        try: self.conduit_pipes_f.disable()  # noqa : E701
        except Exception: pass  # noqa : E701
        finally: del self._conduit_pipes_f  # noqa : E701

        try: self.conduit_pipes_q.disable()  # noqa : E701
        except Exception: pass  # noqa : E701
        finally: del self._conduit_pipes_q  # noqa : E701

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

    # ======================================================================
    # Vertices
    # --------
    # Draw the vertices and add them to the vertex group.
    # Free vertices and anchored vertices are drawn separately.
    # ======================================================================

    def _draw_vertices(self):

        free = list(self.mesh.vertices_where(is_anchor=False))
        fixed = list(self.mesh.vertices_where(is_fixed=True))
        anchors = list(self.mesh.vertices_where(is_anchor=True))

        color_free = self.settings['color.vertices'] if self.is_valid else self.settings['color.invalid']
        color_fixed = self.settings['color.vertices:is_fixed']
        color_anchor = self.settings['color.vertices:is_anchor']

        vertex_color = {vertex: color_free for vertex in free}
        vertex_color.update({vertex: color_fixed for vertex in fixed})
        vertex_color.update({vertex: color_anchor for vertex in anchors})

        guids_free = []
        guids_anchor = []

        if free:
            guids_free = self.artist.draw_vertices(vertices=free, color=vertex_color)
        if anchors:
            guids_anchor = self.artist.draw_vertices(vertices=anchors, color=vertex_color)

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
        vertices = free + anchors

        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

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

        # # draw q pipes
        # if self.settings['_is.valid'] and self.settings['show.pipes:forcedensities']:

        #     xyz = {vertex: self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.vertices()}
        #     edges = list(self.mesh.edges_where({'_is_edge': True}))
        #     color = {edge: self.settings['color.pipes'] for edge in edges}
        #     qs = {edge: self.mesh.edge_attribute(edge, 'q') for edge in edges}

        #     qmin = min(qs.values())
        #     qmax = max(qs.values())
        #     q_range = qmax - qmin or 1

        #     tmin = self.settings['pipe_thickness.min']
        #     tmax = self.settings['pipe_thickness.max']
        #     t_range = tmax - tmin

        #     qs_remapped = {edge: (((q - qmin) * t_range) / q_range) + tmin for edge, q in qs.iteritems()}

        #     for edge in edges:
        #         if qs[edge] >= 0.0:
        #             color[edge] = i_to_red((qs[edge]) / qmax)
        #         elif qs[edge] < 0.0:
        #             color[edge] = i_to_blue((qs[edge]) / qmin)

        #     self.conduit_pipes_q.xyz = xyz
        #     self.conduit_pipes_q.edges = edges
        #     self.conduit_pipes_q.values = qs_remapped
        #     self.conduit_pipes_q.color = color
        #     self.conduit_pipes_q.enable()

        # else:
        #     if self.conduit_pipes_q:
        #         try:
        #             self.conduit_pipes_q.disable()
        #         except Exception:
        #             pass
