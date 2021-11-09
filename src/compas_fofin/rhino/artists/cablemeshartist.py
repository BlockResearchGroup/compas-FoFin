from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import sqrt

import compas_rhino

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector_sqrd

from compas_rhino.artists import MeshArtist


class CableMeshArtist(MeshArtist):
    """Artist for visualizing a CableMesh in the Rhino model space."""

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xy') + [0.0] for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    def draw_reactions(self, vertices, color, scale, tol):
        """Draw the reaction forces at the anchored vertices of the mesh.

        Parameters
        ----------
        vertices : list of int
            The vertices for which the reactions should be drawn.
        color : list or tuple
            The RGB color specification for reaction forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the reaction force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding reaction force vector in Rhino.

        Notes
        -----
        The residual force components are stored per vertex in the `_rx`, `_ry`, and `_rz` attributes.

        """
        vertex_xyz = self.vertex_xyz
        lines = []
        tol2 = tol ** 2

        for vertex in vertices:
            a = vertex_xyz[vertex]
            r = self.mesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -scale)
            if length_vector_sqrd(r) < tol2:
                continue
            b = add_vectors(a, r)
            lines.append({'start': b, 'end': a, 'color': color, 'arrow': "start"})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_loads(self, vertices, color, scale, tol):
        """Draw the externally applied loads at all vertices of the mesh.

        Parameters
        ----------
        vertices : list of int
            The vertices for which the loads should be drawn.
        color : list or tuple
            The RGB color specification for load forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the load force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding load force vector in Rhino.

        Notes
        -----
        The load components are stored per vertex in the `px`, `py`, and `pz` attributes.

        """
        vertex_xyz = self.vertex_xyz
        lines = []
        tol2 = tol ** 2

        for vertex in vertices:
            a = vertex_xyz[vertex]
            p = self.mesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            p = scale_vector(p, scale)
            if length_vector_sqrd(p) < tol2:
                continue
            b = add_vectors(a, p)
            lines.append({'start': b, 'end': a, 'color': color, 'arrow': "start"})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_pipes(self, edges, size, color, scale, tol):
        """Draw pipes around the edges with a radius proportional to the axial force.

        Parameters
        ----------
        edges : list of tuple of int
            The list of edges for which the pipes should be drawn.
        size : float or dict
            The size of the pipes as a single value or as a mapping between edges and sizes.
        color : rgb tuple or dict of rgb tuples
            The color of the pipes a a single value or as a mapping between edges and colors.
        scale : float
            Scaling factor for the forces.
        tol : float
            Minimum diameter of a pipe.

        Returns
        -------
        list of guid
            The identifiers of the cylinder objects in Rhino.
        """
        vertex_xyz = self.vertex_xyz
        cylinders = []
        for edge in edges:
            u, v = edge
            start = vertex_xyz[u]
            end = vertex_xyz[v]

            if isinstance(size, dict):
                pipe_size = size[edge]
            else:
                pipe_size = size

            if pipe_size < 0:
                pipe_size = -pipe_size

            pipe_size = scale * pipe_size

            if pipe_size < tol:
                continue

            radius = sqrt(pipe_size / pi)

            if isinstance(color, dict):
                pipe_color = color[edge]
            else:
                pipe_color = color

            cylinders.append({
                'start': start,
                'end': end,
                'radius': radius,
                'color': pipe_color
            })
        return compas_rhino.draw_cylinders(cylinders, layer=self.layer, clear=False, redraw=False)
