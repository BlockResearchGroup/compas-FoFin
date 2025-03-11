from pydantic import BaseModel

from compas_session.settings import Settings


class SolverSettings(BaseModel):
    kmax: int = 100
    tol_residuals: float = 1e-3
    tol_displacements: float = 1e-3
    damping: float = 0.1


class DrawingSettings(BaseModel):
    """These apply to conventional drawing processes."""

    edge_thickness: int = 1

    show_loads: bool = False
    show_selfweight: bool = False
    show_reactions: bool = True
    show_residuals: bool = False
    show_forces: bool = True

    scale_loads: float = 1.0
    scale_reactions: float = 1e-1
    scale_residuals: float = 1.0
    scale_forces: float = 1e-3

    tol_loads: float = 1e-3
    tol_reactions: float = 1e-3
    tol_residuals: float = 1e-3
    tol_forces: float = 1e-3


class DisplaySettings(BaseModel):
    """These apply to conduits specifically."""

    tmax: int = 10


class FoFinSettings(Settings):
    solver: SolverSettings = SolverSettings()
    drawing: DrawingSettings = DrawingSettings()
    display: DisplaySettings = DisplaySettings()
