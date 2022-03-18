from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.artists import MeshArtist
from compas.colors import Color


class CableMeshArtist(MeshArtist):
    """Base artist for visualizing a CableMesh.

    Parameters
    ----------
    cablemesh : :class:`compas_fofin.datastructures.CableMesh`

    """

    def __init__(self, *args, **kwargs):
        super(CableMeshArtist, self).__init__(*args, **kwargs)

    @abstractmethod
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
        list[...]
            The identifiers of the objects representing the reaction forces in the scene.

        """
        raise NotImplementedError

    @abstractmethod
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
        list[...]
            The identifiers of the objects representing the loads in the scene.

        """
        raise NotImplementedError

    @abstractmethod
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
        list[...]
            The identifiers of the objects representing the pipes in the scene.

        """
        raise NotImplementedError
