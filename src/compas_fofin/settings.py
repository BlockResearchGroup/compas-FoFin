# from compas_rui.values import BoolValue
# from compas_rui.values import FloatValue
# from compas_rui.values import IntValue
# from compas_rui.values import Settings

# SETTINGS = {
#     "FormFinder": Settings(
#         {
#             "autosave.events": BoolValue(True),
#             "autoupdate.constraints": BoolValue(False),
#         }
#     ),
#     "Solvers": Settings(
#         {
#             "constraints.maxiter": IntValue(100),
#         }
#     ),
# }

import json
from dataclasses import dataclass
from dataclasses import field
from dataclasses import is_dataclass


class SettingsBase:
    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as fp:
            data: dict = json.load(fp)
        config = cls(**data)
        return config

    def to_json(self, filepath):
        with open(filepath, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                data[key] = value.to_dict() if hasattr(value, "to_dict") else value
        return data

    def __post_init__(self):
        for field_name, field_value in self.__dict__.items():
            field_type = self.__annotations__[field_name]
            if isinstance(field_value, dict) and is_dataclass(field_type):
                # Convert dict to dataclass if the field type is a dataclass
                setattr(self, field_name, field_type(**field_value))
            elif isinstance(field_value, dict) and not is_dataclass(field_type):
                raise ValueError(f"Expected dataclass type for field '{field_name}' but got dict.")


@dataclass
class SolverSettings(SettingsBase):
    kmax: int = 100
    tol_residuals: float = 1e-3
    tol_displacements: float = 1e-3
    damping: float = 0.1


@dataclass
class DrawingSettings(SettingsBase):
    """These apply to conventional drawing processes."""

    show_reactions: bool = True
    show_forces: bool = True
    show_residuals: bool = False
    show_loads: bool = False
    scale_reactions: float = 1e-1

    # _scale_reactions: float = field(init=False, repr=False)

    # @property
    # def scale_reactions(self) -> float:
    #     return self._scale_reactions

    # @scale_reactions.setter
    # def scale_reactions(self, value: float) -> None:
    #     self._scale_reactions = min(max(value, 1e-3), 1e3)


@dataclass
class DisplaySettings(SettingsBase):
    """These apply to conduits specifically."""

    tmax: int = 10


@dataclass
class Settings(SettingsBase):
    solver: SolverSettings = field(default_factory=SolverSettings)
    drawing: DrawingSettings = field(default_factory=DrawingSettings)
    display: DisplaySettings = field(default_factory=DisplaySettings)
    autosave: bool = True
