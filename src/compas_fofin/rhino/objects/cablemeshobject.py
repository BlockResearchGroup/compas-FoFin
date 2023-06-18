from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from math import fabs

import System
import Rhino
import compas_rhino

from compas.colors import Color
from compas.colors import ColorMap
from compas.artists import Artist

from compas_ui.rhino.objects import RhinoMeshObject

from compas_fofin.objects import CableMeshObject
from compas_fofin.rhino.conduits import ReactionConduit
from compas_fofin.rhino.conduits import LoadConduit
from compas_fofin.rhino.conduits import SelfweightConduit
from compas_fofin.rhino.conduits import PipeConduit
from compas_fofin.rhino.conduits import EdgeConduit
from compas_fofin.rhino.conversions import curveobject_to_compas

RED = ColorMap.from_two_colors(Color.white(), Color.red())
BLUE = ColorMap.from_two_colors(Color.white(), Color.blue())


class RhinoCableMeshObject(CableMeshObject, RhinoMeshObject):
    """Scene object for FF CableMeshes.

    Attributes
    ----------
    group_free : str
        The name of the group containing all free vertices.
    group_fixed : str
        The name of the group containing all fixed vertices.
    group_anchors : str
        The name of the group containing all anchored vertices.
    group_edges : str
        The name of the group containing all edges.
    group_faces : str
        The name of the group containing all faces.
    conduit_reactions : :class:`compas_fofin.rhino.conduits.ReactionConduit`
        Conduit for visualizing reaction forces.
    conduit_loads : :class:`compas_fofin.rhino.conduits.LoadConduit`
        Conduit for visualizing loads.
    conduit_forces : :class:`compas_fofin.rhino.conduits.PipeConduit`
        Conduit for visualizing axial forces.
    conduit_forcedensities : :class:`compas_fofin.rhino.conduits.PipeConduit`
        Conduit for visualizing force densities.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoCableMeshObject, self).__init__(*args, **kwargs)
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_selfweight = None
        self._conduit_forces = None
        self._conduit_forcedensities = None
        self._conduit_edges = None

    @property
    def group_free(self):
        if not self._group_free:
            group = "{}::vertices::free".format(self.guid)
            self._group_free = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_free

    @property
    def group_fixed(self):
        if not self._group_fixed:
            group = "{}::vertices::fixed".format(self.guid)
            self._group_fixed = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_fixed

    @property
    def group_anchors(self):
        if not self._group_anchors:
            group = "{}::vertices::anchors".format(self.guid)
            self._group_anchors = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_anchors

    @property
    def group_edges(self):
        if not self._group_edges:
            group = "{}::edges".format(self.guid)
            self._group_edges = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_edges

    @property
    def group_faces(self):
        if not self._group_faces:
            group = "{}::faces".format(self.guid)
            self._group_faces = group

            if not compas_rhino.rs.IsGroup(group):
                compas_rhino.rs.AddGroup(group)

        return self._group_faces

    @property
    def conduit_reactions(self):
        if not self._conduit_reactions:
            self._conduit_reactions = ReactionConduit(
                self.mesh,
                color=self.settings["color.reactions"].rgb255,
                scale=self.settings["scale.reactions"],
                tol=self.settings["tol.externalforces"],
            )
        return self._conduit_reactions

    @property
    def conduit_loads(self):
        if not self._conduit_loads:
            self._conduit_loads = LoadConduit(
                self.mesh,
                color=self.settings["color.loads"].rgb255,
                scale=self.settings["scale.loads"],
                tol=self.settings["tol.externalforces"],
            )
        return self._conduit_loads

    @property
    def conduit_selfweight(self):
        if not self._conduit_selfweight:
            self._conduit_selfweight = SelfweightConduit(
                self.mesh,
                color=self.settings["color.selfweight"].rgb255,
                scale=self.settings["scale.selfweight"],
                tol=self.settings["tol.externalforces"],
            )
        return self._conduit_selfweight

    @property
    def conduit_forces(self):
        if not self._conduit_forces:
            self._conduit_forces = PipeConduit(xyz={}, edges=[], values={}, color={})
        return self._conduit_forces

    @property
    def conduit_forcedensities(self):
        if not self._conduit_forcedensities:
            self._conduit_forcedensities = PipeConduit(xyz={}, edges=[], values={}, color={})
        return self._conduit_forcedensities

    @property
    def conduit_edges(self):
        if not self._conduit_edges:
            vertex_index = self.mesh.key_index()
            edges = self.mesh.edges_where(_is_edge=True)
            edges = [(vertex_index[u], vertex_index[v]) for u, v in edges]
            xyz = self.mesh.vertices_attributes("xyz")
            self._conduit_edges = EdgeConduit(xyz, edges)
        return self._conduit_edges

    # ======================================================================
    # Methods
    # ======================================================================

    def update_constraint(self, vertex, constraint, obj):
        """
        Update a vertex constraint using the current geometr of a given constraint object.

        Parameters
        ----------
        vertex : int
        constraint
        obj : RhinoObject

        Returns
        -------
        None

        """
        if str(obj.Id) != constraint._rhino_guid:
            return

        point = self.mesh.vertex_attributes(vertex, "xyz")

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:
            curve = curveobject_to_compas(obj)
            constraint.geometry = curve

        elif obj.ObjectType == Rhino.DocObjects.ObjectType.Surface:
            raise NotImplementedError

        constraint.location = point
        constraint.project()
        self.mesh.vertex_attributes(vertex, "xyz", constraint.location)

    def update_constraints(self):
        """
        Update all constraints to the latest constraint geometry.

        Returns
        -------
        None

        """
        for vertex in self.mesh.vertices_where(is_anchor=True):
            # check if a vertex has a constraint
            constraint = self.mesh.vertex_attribute(vertex, "constraint")
            if not constraint or not constraint._rhino_guid:
                continue

            # convert the guid string to an object
            result, guid = System.Guid.TryParse(constraint._rhino_guid)
            if not result:
                continue

            # find the object corresponding to the guid
            obj = compas_rhino.find_object(guid)
            if not obj:
                continue

            # update the vertex
            self.update_constraint(vertex, constraint, obj)

    def update_equilibrium(self, ui, kmax=None):
        """
        Update the equilibrium of the cablemesh.

        Returns
        -------
        bool

        """
        fd = ui.proxy.function("compas_fd.fd.mesh_fd_constrained_numpy")
        kmax = kmax or ui.registry["FoFin"]["solver.kmax"]

        result = fd(
            self.mesh,
            kmax=kmax,
            damping=ui.registry["FoFin"]["solver.damping"],
            tol_res=ui.registry["FoFin"]["solver.tol.residuals"],
            tol_disp=ui.registry["FoFin"]["solver.tol.displacements"],
        )

        if not result:
            print("Force-density method equilibrium failed!")
            return False

        self.mesh.data = result.data
        self.is_valid = True

        return True

    # ======================================================================
    # Clear
    # ======================================================================

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
            self.conduit_selfweight.disable()
        except Exception:
            pass
        finally:
            del self._conduit_selfweight
            self._conduit_selfweight = None

        try:
            self.conduit_forces.disable()
        except Exception:
            pass
        finally:
            del self._conduit_forces
            self._conduit_forces = None

        try:
            self.conduit_forcedensities.disable()
        except Exception:
            pass
        finally:
            del self._conduit_forcedensities
            self._conduit_forcedensities = None

        try:
            self.conduit_edges.disable()
        except Exception:
            pass
        finally:
            del self._conduit_edges
            self._conduit_edges = None

    def clear(self):
        super(CableMeshObject, self).clear()
        self.clear_conduits()

    # ======================================================================
    # Draw
    # ======================================================================

    def draw(self):
        layer = self.layer
        self.artist.layer = layer

        self.clear()
        if not self.visible:
            return

        self.artist.vertex_xyz = self.vertex_xyz

        self._draw_vertices()
        self._draw_edges()
        self._draw_faces()

        self._draw_constraints()

        self._draw_reaction_overlays()
        self._draw_load_overlays()
        self._draw_selfweight_overlays()
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
        constrained = list(self.mesh.vertices_where_predicate(lambda key, attr: attr["constraint"] is not None))

        color_free = self.settings["color.vertices"]
        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchored = self.settings["color.vertices:is_anchor"]
        color_constrained = self.settings["color.vertices:is_constrained"]

        color = {vertex: color_free for vertex in free}
        color.update({vertex: color_fixed for vertex in fixed})
        color.update({vertex: color_anchored for vertex in anchored})
        color.update({vertex: color_constrained for vertex in constrained})

        guids_free = []
        guids_anchor = []

        if free:
            guids_free = self.artist.draw_vertices(free, color)
        if anchored:
            guids_anchor = self.artist.draw_vertices(anchored, color)

        compas_rhino.rs.AddObjectsToGroup(guids_free, self.group_free)
        compas_rhino.rs.AddObjectsToGroup(guids_anchor, self.group_anchors)

        if self.settings["show.vertices:is_anchor"]:
            compas_rhino.rs.ShowGroup(self.group_anchors)
        else:
            compas_rhino.rs.HideGroup(self.group_anchors)

        if self.settings["show.vertices:free"]:
            compas_rhino.rs.ShowGroup(self.group_free)
        else:
            compas_rhino.rs.HideGroup(self.group_free)

        guids = guids_free + guids_anchor
        vertices = free + anchored

        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

    # ======================================================================
    # Edges
    # -----
    # Draw the edges and add them to the edge group.
    # ======================================================================

    def _draw_edges(self):
        edges = list(self.mesh.edges_where(_is_edge=True))
        color = {edge: self.settings["color.edges"] for edge in edges}

        if self.is_valid:
            edge_q = {edge: self.mesh.edge_attribute(edge, "q") for edge in edges}
            for edge in edges:
                if edge_q[edge] < 0.0:
                    color[edge] = self.settings["color.compression"]
                else:
                    color[edge] = self.settings["color.tension"]

        guids = self.artist.draw_edges(edges, color)
        compas_rhino.rs.AddObjectsToGroup(guids, self.group_edges)

        if self.show_edges:
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
        if self.settings["show.faces:all"]:
            faces = list(self.mesh.faces())
        else:
            faces = list(self.mesh.faces_where(is_loaded=True))

        if faces:
            color = {face: self.settings["color.faces"] for face in faces}
            guids = self.artist.draw_faces(faces, color)

            compas_rhino.rs.AddObjectsToGroup(guids, self.group_faces)

            if self.settings["show.faces"]:
                compas_rhino.rs.ShowGroup(self.group_faces)
            else:
                compas_rhino.rs.HideGroup(self.group_faces)

            self.guids += guids
            self.guid_face = zip(guids, faces)

    # ======================================================================
    # Constraints
    # -----------
    # Draw the constraints if they are not alreay in the model.
    # ======================================================================

    def _draw_constraints(self):
        old_new = {}

        for vertex in self.mesh.vertices():
            constraint = self.mesh.vertex_attribute(vertex, "constraint")
            if constraint is not None:
                guid = constraint._rhino_guid

                if not guid:
                    # this constraint doesn't have a corresponding Rhino object
                    artist = Artist(constraint)
                    guids = artist.draw()
                    guid = guids[0]
                    constraint._rhino_guid = str(guid)

                elif guid in old_new:
                    # this constraint has a corresponding Rhino object
                    # that has already been processed.
                    constraint._rhino_guid = old_new[guid]

                else:
                    # this constraint has a corresponding Rhino object
                    result, guid = System.Guid.TryParse(guid)

                    if result:
                        obj = compas_rhino.find_object(guid)

                        if obj:
                            # the Rhino object exists in the model
                            # we just change the color
                            compas_rhino.rs.ObjectColor(guid, Color.cyan().rgb255)

                        else:
                            # the Rhino object doesn't exist
                            # so we create it and assign the new GUID to the consttraint
                            # we keep track of the relationship between old and new GUID
                            # to update other constraints accordingly
                            artist = Artist(constraint)
                            guids = artist.draw()
                            guid = str(guids[0])
                            old_new[constraint._rhino_guid] = guid
                            constraint._rhino_guid = guid

    # ======================================================================
    # Overlays
    # --------
    # Color overlays for various display modes.
    # ======================================================================

    def _draw_reaction_overlays(self):
        self.conduit_reactions.disable()
        if self.is_valid and self.settings["show.reactions"]:
            self.conduit_reactions.color = self.settings["color.reactions"].rgb255
            self.conduit_reactions.scale = self.settings["scale.reactions"]
            self.conduit_reactions.tol = self.settings["tol.externalforces"]
            self.conduit_reactions.enable()

    def _draw_load_overlays(self):
        self.conduit_loads.disable()
        if self.settings["show.loads"]:
            self.conduit_loads.color = self.settings["color.loads"].rgb255
            self.conduit_loads.scale = self.settings["scale.loads"]
            self.conduit_loads.tol = self.settings["tol.externalforces"]
            self.conduit_loads.enable()

    def _draw_selfweight_overlays(self):
        self.conduit_selfweight.disable()
        if self.settings["show.selfweight"]:
            self.conduit_selfweight.color = self.settings["color.selfweight"].rgb255
            self.conduit_selfweight.scale = self.settings["scale.selfweight"]
            self.conduit_selfweight.tol = self.settings["tol.externalforces"]
            self.conduit_selfweight.enable()

    def _draw_force_overlays(self):
        self.conduit_forces.disable()

        if self.is_valid and self.settings["show.pipes:forces"]:
            xyz = {v: self.mesh.vertex_coordinates(v) for v in self.mesh.vertices()}
            edges = list(self.mesh.edges_where(_is_edge=True))
            forces = self.mesh.edges_attribute("_f", keys=edges)

            fmin = min(forces)
            fmax = max(forces)
            frange = (fmax - fmin) or 1

            color = {e: self.settings["color.pipes"].rgb255 for e in edges}

            if fmin != fmax:
                for e, f in zip(edges, forces):
                    if f >= 0.0:
                        color[e] = RED(f / fmax).rgb255
                    elif f < 0.0:
                        color[e] = BLUE(f / fmin).rgb255

            forces = [fabs(f) for f in forces]
            fmin = min(forces)
            tmin = self.settings["pipe_thickness.min"]
            tmax = self.settings["pipe_thickness.max"]
            trange = tmax - tmin
            r = trange / frange

            remapped = {e: ((f - fmin) * r) + tmin for e, f in zip(edges, forces)}

            self.conduit_forces.xyz = xyz
            self.conduit_forces.edges = edges
            self.conduit_forces.values = remapped
            self.conduit_forces.color = color
            self.conduit_forces.enable()

    def _draw_q_overlays(self):
        self.conduit_forcedensities.disable()

        if self.is_valid and self.settings["show.pipes:forcedensities"]:
            xyz = {v: self.mesh.vertex_coordinates(v) for v in self.mesh.vertices()}
            edges = list(self.mesh.edges_where(_is_edge=True))
            qs = self.mesh.edges_attribute("q", keys=edges)

            qmin = min(qs)
            qmax = max(qs)
            qrange = (qmax - qmin) or 1

            color = {edge: self.settings["color.pipes"].rgb255 for edge in edges}

            if qmin != qmax:
                for e, q in zip(edges, qs):
                    if q >= 0.0:
                        color[e] = RED(q / qmax).rgb255
                    elif q < 0.0:
                        color[e] = BLUE(q / qmin).rgb255

            qs = [fabs(q) for q in qs]
            qmin = min(q)
            tmin = self.settings["pipe_thickness.min"]
            tmax = self.settings["pipe_thickness.max"]
            trange = tmax - tmin
            r = trange / qrange

            remapped = {e: ((q - qmin) * r) + tmin for e, q in zip(edges, qs)}

            self.conduit_forcedensities.xyz = xyz
            self.conduit_forcedensities.edges = edges
            self.conduit_forcedensities.values = remapped
            self.conduit_forcedensities.color = color
            self.conduit_forcedensities.enable()
