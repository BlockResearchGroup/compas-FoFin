from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.utilities import i_to_red, i_to_blue, normalize_values
import compas_rhino

from .meshobject import MeshObject

from compas_fofin.rhino import ReactionConduit
from compas_fofin.rhino import LoadConduit
from compas_fofin.rhino import PipeConduit


class CableMeshObject(MeshObject):
    """Scene object for FF CableMeshes.
    """

    SETTINGS = {
        '_is.valid': False,
        'layer': "FF::CableMesh",
        'show.vertices:is_anchor': True,
        'show.vertices:free': False,
        'show.edges': True,
        'show.faces': True,
        'show.faces:all': False,
        'show.reactions': True,
        'show.loads': True,
        'show.pipes:forcedensities': False,
        'show.pipes:forces': False,

        'color.vertices': [255, 255, 255],
        'color.vertices:is_anchor': [255, 0, 0],
        'color.vertices:is_fixed': [0, 0, 255],
        'color.vertices:is_constrained': [0, 255, 255],
        'color.edges': [255, 0, 0],
        'color.faces': [200, 200, 200],
        'color.reactions': [0, 200, 0],
        'color.loads': [0, 80, 0],
        'color.invalid': [100, 255, 100],
        'color.pipes': [100, 100, 100],

        'scale.externalforces': 1,

        'pipe_thickness.min': 0,
        'pipe_thickness.max': 10,

        'tol.externalforces': 1e-3,

    }

    def __init__(self, diagram, *args, **kwargs):
        super(CableMeshObject, self).__init__(diagram, *args, **kwargs)
        self._guid_pipes = {}
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_pipes_f = None
        self._conduit_pipes_q = None

    @property
    def vertex_xyz(self):
        """dict : The view coordinates of the mesh object."""
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.mesh.vertex_attributes(self.anchor, 'xyz')
            point = Point(* xyz)
            T1 = Translation.from_vector(origin - point)
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T2 = Translation.from_vector(self.location)
            X = T2 * R * S * T1
        else:
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T = Translation.from_vector(self.location)
            X = T * R * S
        mesh = self.mesh.transformed(X)
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        return vertex_xyz

    @property
    def guids(self):
        guids = super(MeshObject, self).guids
        guids += list(self.guid_pipes.keys())
        return guids

    @property
    def guid_pipes(self):
        """Map between Rhino object GUIDs and reaction identifiers."""
        return self._guid_pipes

    @guid_pipes.setter
    def guid_pipes(self, values):
        self._guid_pipes = dict(values)

    @property
    def conduit_reactions(self):
        if self._conduit_reactions is None:
            conduit_reactions = ReactionConduit(self.mesh,
                                                color=self.settings['color.reactions'],
                                                scale=self.settings['scale.externalforces'],
                                                tol=self.settings['tol.externalforces'])
            self._conduit_reactions = conduit_reactions
        return self._conduit_reactions

    @property
    def conduit_loads(self):
        if self._conduit_loads is None:
            conduit_loads = LoadConduit(self.mesh,
                                        color=self.settings['color.loads'],
                                        scale=self.settings['scale.externalforces'],
                                        tol=self.settings['tol.externalforces'])
            self._conduit_loads = conduit_loads
        return self._conduit_loads

    @property
    def conduit_pipes_f(self):
        if self._conduit_pipes_f is None:
            conduit_pipes_f = PipeConduit(xyz={}, edges=[], values={}, color={})
            self._conduit_pipes_f = conduit_pipes_f
        return self._conduit_pipes_f

    @property
    def conduit_pipes_q(self):
        if self._conduit_pipes_q is None:
            conduit_pipes_q = PipeConduit(xyz={}, edges=[], values={}, color={})
            self._conduit_pipes_q = conduit_pipes_q
        return self._conduit_pipes_q

    def clear_conduits(self):
        try:
            self.conduit_reactions.disable()
        except Exception:
            pass
        finally:
            del self._conduit_reactions

        try:
            self.conduit_loads.disable()
        except Exception:
            pass
        finally:
            del self._conduit_loads

        try:
            self.conduit_pipes_f.disable()
        except Exception:
            pass
        finally:
            del self._conduit_pipes_f

        try:
            self.conduit_pipes_q.disable()
        except Exception:
            pass
        finally:
            del self._conduit_pipes_q

    def draw(self):
        """Draw the objects representing the cablemesh.
        """
        layer = self.settings['layer']
        self.artist.layer = layer
        self.artist.clear_layer()
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        # ======================================================================
        # Groups
        # ------
        # Create groups for free and anchored vertices, edges, and faces.
        # These groups will be turned on/off based on the visibility settings of the mesh
        # ======================================================================

        group_free = "{}::vertices_free".format(layer)
        group_anchor = "{}::vertices_anchor".format(layer)

        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        if not compas_rhino.rs.IsGroup(group_free):
            compas_rhino.rs.AddGroup(group_free)

        if not compas_rhino.rs.IsGroup(group_anchor):
            compas_rhino.rs.AddGroup(group_anchor)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        # ======================================================================
        # Vertices
        # --------
        # Draw the vertices and add them to the vertex group.
        # Free vertices and anchored vertices are drawn separately.
        # ======================================================================

        free = list(self.mesh.vertices_where({'is_anchor': False}))
        anchors = list(self.mesh.vertices_where({'is_anchor': True}))
        color_free = self.settings['color.vertices'] if self.settings['_is.valid'] else self.settings['color.invalid']
        color_fixed = self.settings['color.vertices:is_fixed']
        color_anchor = self.settings['color.vertices:is_anchor']
        color = {vertex: color_free for vertex in free}
        color.update({vertex: color_fixed for vertex in self.mesh.vertices_where({'is_fixed': True})})
        color.update({vertex: color_anchor for vertex in anchors})

        if free:
            guids_free = self.artist.draw_vertices(free, color)
        else:
            guids_free = []
        if anchors:
            guids_anchor = self.artist.draw_vertices(anchors, color)
        else:
            guids_anchor = []
        self.guid_vertex = zip(guids_free + guids_anchor, free + anchors)
        compas_rhino.rs.AddObjectsToGroup(guids_free, group_free)
        compas_rhino.rs.AddObjectsToGroup(guids_anchor, group_anchor)

        if self.settings['show.vertices:is_anchor']:
            compas_rhino.rs.ShowGroup(group_anchor)
        else:
            compas_rhino.rs.HideGroup(group_anchor)

        if self.settings['show.vertices:free']:
            compas_rhino.rs.ShowGroup(group_free)
        else:
            compas_rhino.rs.HideGroup(group_free)

        # ======================================================================
        # Edges
        # -----
        # Draw the edges and add them to the edge group.
        # ======================================================================

        edges = list(self.mesh.edges_where({'_is_edge': True}))
        if self.settings['_is.valid']:
            qs = {edge: self.mesh.edge_attribute(edge, 'q') for edge in edges}
            color = {edge: self.settings['color.edges'] for edge in edges}
            for edge in edges:
                if qs[edge] < 0.0:
                    color[edge] = [0, 0, 255]
        else:
            color = {edge: self.settings['color.invalid'] for edge in edges}

        guids = self.artist.draw_edges(edges, color)
        self.guid_edge = zip(guids, edges)
        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings['show.edges']:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        # ======================================================================
        # Faces
        # -----
        # Draw the faces and add them to the face group.
        # ======================================================================

        if self.settings['show.faces:all']:
            faces = list(self.mesh.faces())
        else:
            faces = list(self.mesh.faces_where({'is_loaded': True}))
        color = {face: self.settings['color.faces'] for face in faces}

        if faces:
            guids = self.artist.draw_faces(faces, color)
            self.guid_face = zip(guids, faces)
            compas_rhino.rs.AddObjectsToGroup(guids, group_faces)

            if self.settings['show.faces']:
                compas_rhino.rs.ShowGroup(group_faces)
            else:
                compas_rhino.rs.HideGroup(group_faces)

        # self.redraw()

        # ======================================================================
        # Overlays
        # --------
        # Color overlays for various display modes.
        # ======================================================================

        # draw reactions
        if self.settings['_is.valid'] and self.settings['show.reactions']:
            self.conduit_reactions.enable()
        else:
            if self.conduit_reactions:
                try:
                    self.conduit_reactions.disable()
                except Exception:
                    pass

        # draw loads
        if self.settings['show.loads']:
            self.conduit_loads.enable()
        else:
            if self.conduit_loads:
                try:
                    self.conduit_loads.disable()
                except Exception:
                    pass

        # draw force pipes
        if self.settings['_is.valid'] and self.settings['show.pipes:forces']:

            xyz = {vertex: self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.vertices()}
            edges = list(self.mesh.edges_where({'_is_edge': True}))
            color = {edge: self.settings['color.pipes'] for edge in edges}
            forces = {edge: self.mesh.edge_attribute(edge, '_f') for edge in edges}

            fmin = min(forces.values())
            fmax = max(forces.values())
            f_range = fmax - fmin or 1

            tmin = self.settings['pipe_thickness.min']
            tmax = self.settings['pipe_thickness.max']
            t_range = tmax - tmin

            forces_remapped = {edge: (((f - fmin) * t_range) / f_range) + tmin for edge, f in forces.iteritems()}

            for edge in edges:
                if fmin != fmax:
                    if forces[edge] >= 0.0:
                        color[edge] = i_to_red((forces[edge]) / fmax)
                    elif forces[edge] < 0.0:
                        color[edge] = i_to_blue((forces[edge]) / fmin)

            self.conduit_pipes_f.xyz = xyz
            self.conduit_pipes_f.edges = edges
            self.conduit_pipes_f.values = forces_remapped
            self.conduit_pipes_f.color = color
            self.conduit_pipes_f.enable()

        else:
            if self.conduit_pipes_f:
                try:
                    self.conduit_pipes_f.disable()
                except Exception:
                    pass

        # draw q pipes
        if self.settings['_is.valid'] and self.settings['show.pipes:forcedensities']:

            xyz = {vertex: self.mesh.vertex_coordinates(vertex) for vertex in self.mesh.vertices()}
            edges = list(self.mesh.edges_where({'_is_edge': True}))
            color = {edge: self.settings['color.pipes'] for edge in edges}
            qs = {edge: self.mesh.edge_attribute(edge, 'q') for edge in edges}

            qmin = min(qs.values())
            qmax = max(qs.values())
            q_range = qmax - qmin or 1

            tmin = self.settings['pipe_thickness.min']
            tmax = self.settings['pipe_thickness.max']
            t_range = tmax - tmin

            qs_remapped = {edge: (((q - qmin) * t_range) / q_range) + tmin for edge, q in qs.iteritems()}

            for edge in edges:
                if qs[edge] >= 0.0:
                    color[edge] = i_to_red((qs[edge]) / qmax)
                elif qs[edge] < 0.0:
                    color[edge] = i_to_blue((qs[edge]) / qmin)

            self.conduit_pipes_q.xyz = xyz
            self.conduit_pipes_q.edges = edges
            self.conduit_pipes_q.values = qs_remapped
            self.conduit_pipes_q.color = color
            self.conduit_pipes_q.enable()

        else:
            if self.conduit_pipes_q:
                try:
                    self.conduit_pipes_q.disable()
                except Exception:
                    pass
