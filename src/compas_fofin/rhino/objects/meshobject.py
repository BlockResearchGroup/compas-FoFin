from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import add_vectors

import compas_rhino
from compas_rhino.objects import MeshObject
from compas_rhino.objects import mesh_update_vertex_attributes
from compas_rhino.objects import mesh_update_edge_attributes
from compas_rhino.objects import mesh_update_face_attributes

from compas_fofin.rhino import select_vertices
from compas_fofin.rhino import select_faces
from compas_fofin.rhino import select_edges


__all__ = ['MeshObject']


class MeshObject(MeshObject):
    """Scene object for mesh-based data structures in FF.
    """

    @property
    def datastructure(self):
        return self.mesh

    @datastructure.setter
    def datastructure(self, datastructure):
        self.mesh = datastructure

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

    def update_attributes(self):
        """Update the attributes of the data structure through a Rhino dialog.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        return compas_rhino.update_settings(self.datastructure.attributes)

    def update_vertices_attributes(self, keys, names=None):
        """Update the attributes of selected vertices.

        Parameters
        ----------
        keys : list
            The identifiers of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            select_vertices(self.datastructure, keys)
            return mesh_update_vertex_attributes(self.datastructure, keys, names)

    def update_edges_attributes(self, keys, names=None):
        """Update the attributes of selected edges.

        Parameters
        ----------
        keys : list
            The identifiers of the edges of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            select_edges(self.datastructure, keys)
            return mesh_update_edge_attributes(self.datastructure, keys, names)

    def update_faces_attributes(self, keys, names=None):
        """Update the attributes of selected faces.

        Parameters
        ----------
        keys : list
            The identifiers of the faces of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is ``None``, in which case all attributes are updated.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        if keys:
            compas_rhino.rs.UnselectAllObjects()
            select_faces(self.datastructure, keys)
            return mesh_update_face_attributes(self.datastructure, keys, names)

    def move_vertices_vertical(self, keys):
        """Move selected vertices along the Z axis.

        Parameters
        ----------
        keys : list
            The identifiers of the vertices.
        """
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

        Point3d = Rhino.Geometry.Point3d
        Vector3d = Rhino.Geometry.Vector3d
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for key in keys:
            a = self.datastructure.vertex_coordinates(key)
            nbrs = self.datastructure.vertex_neighbors(key)
            for nbr in nbrs:
                b = self.datastructure.vertex_coordinates(nbr)
                line = [Point3d(*a), Point3d(*b)]
                if nbr in keys:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move from?')
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()
        vector = Vector3d(0, 0, 1)

        gp.SetCommandPrompt('Point to move to?')
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Constrain(Rhino.Geometry.Line(start, start + vector))
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = list(end - start)
        for key in keys:
            xyz = self.datastructure.vertex_attributes(key, 'xyz')
            self.datastructure.vertex_attributes(key, 'xyz', add_vectors(xyz, vector))

        return True

    def move_vertices_horizontal(self, keys):
        """Move selected vertices in a horizontal plane.

        Parameters
        ----------
        keys : list
            The identifiers of the vertices.
        """
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

        Point3d = Rhino.Geometry.Point3d
        Vector3d = Rhino.Geometry.Vector3d
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for key in keys:
            a = self.datastructure.vertex_coordinates(key)
            nbrs = self.datastructure.vertex_neighbors(key)
            for nbr in nbrs:
                b = self.datastructure.vertex_coordinates(nbr)
                line = [Point3d(a[0], a[1], 0), Point3d(b[0], b[1], 0)]
                if nbr in keys:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move from?')
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()
        vector = Vector3d(0, 0, 1)

        gp.SetCommandPrompt('Point to move to?')
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Constrain(Rhino.Geometry.Plane(start, vector), False)
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = list(end - start)
        for key in keys:
            xyz = self.datastructure.vertex_attributes(key, 'xyz')
            self.datastructure.vertex_attributes(key, 'xyz', add_vectors(xyz, vector))

        return True
