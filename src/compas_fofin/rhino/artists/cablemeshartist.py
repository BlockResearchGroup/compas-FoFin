from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from math import pi
# from math import sqrt

import compas_rhino

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector_sqrd

from compas.colors import Color

from compas_rhino.artists import MeshArtist
from compas_fofin.artists import CableMeshArtist


class RhinoCableMeshArtist(CableMeshArtist, MeshArtist):
    """Artist for visualizing a CableMesh in the Rhino model space."""

    def draw_reactions(self, color=Color.green(), scale=1e-3, tol=1e-3):
        """Draw the reaction forces at the anchored vertices of the mesh.

        Parameters
        ----------
        color : :class:`compas.colors.Color`, optional
            Color of reaction forces.
        scale : float, optional
            The scaling factor for the reaction force vectors.
        tol : float, optional
            Reaction forces with a scaled length lower than this value will not be drawn.

        Returns
        -------
        list[System.Guid]
            The identifiers of the objects representing the reaction forces in the scene.

        """
        tol2 = tol ** 2
        vertex_xyz = self.vertex_xyz
        lines = []
        for vertex in self.cablemesh.vertices_where(is_anchor=True):
            a = vertex_xyz[vertex]
            r = self.cablemesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'])
            r = scale_vector(r, -scale)
            if length_vector_sqrd(r) < tol2:
                continue
            b = add_vectors(a, r)
            lines.append({'start': b, 'end': a, 'color': color.rgb255, 'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_loads(self, color=Color.blue(), scale=1.0, tol=1e-3):
        """Draw the externally applied loads at all vertices of the mesh.

        Parameters
        ----------
        color : :class:`compas.colors.Color`, optional
            Color of the loads.
        scale : float, optional
            The scaling factor for the load vectors.
        tol : float, optional
            Loads with a scaled length lower than this value will not be drawn.

        Returns
        -------
        list[System.Guid]
            The identifiers of the objects representing the loads in the scene.

        """
        tol2 = tol ** 2
        vertex_xyz = self.vertex_xyz
        lines = []
        for vertex in self.cablemesh.vertices():
            a = vertex_xyz[vertex]
            p = self.cablemesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            p = scale_vector(p, scale)
            if length_vector_sqrd(p) < tol2:
                continue
            b = add_vectors(a, p)
            lines.append({'start': b, 'end': a, 'color': color.rgb255, 'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_pipes(self, color, scale=1e-3, tol=1e-3):
        """Draw pipes around the edges with a radius proportional to the axial force.

        Parameters
        ----------
        color : :class:`compas.colors.Color` | dict[tuple[int, int], :class:`compas.colors.Color`]
            The color of the pipes a a single value or as a mapping between edges and colors.
        scale : float, optional
            Scaling factor for the forces.
        tol : float, optional
            Minimum diameter of a pipe.

        Returns
        -------
        list[System.Guid]
            The identifiers of the objects representing the pipes in the scene.

        """
        # vertex_xyz = self.vertex_xyz
        # cylinders = []
        # for edge in self.cablemesh.edges():
        #     u, v = edge
        #     start = vertex_xyz[u]
        #     end = vertex_xyz[v]

        #     if isinstance(size, dict):
        #         pipe_size = size[edge]
        #     else:
        #         pipe_size = size

        #     if pipe_size < 0:
        #         pipe_size = -pipe_size

        #     pipe_size = scale * pipe_size

        #     if pipe_size < tol:
        #         continue

        #     radius = sqrt(pipe_size / pi)

        #     if isinstance(color, dict):
        #         pipe_color = color[edge]
        #     else:
        #         pipe_color = color

        #     cylinders.append({
        #         'start': start,
        #         'end': end,
        #         'radius': radius,
        #         'color': pipe_color
        #     })
        # return compas_rhino.draw_cylinders(cylinders, layer=self.layer, clear=False, redraw=False)
