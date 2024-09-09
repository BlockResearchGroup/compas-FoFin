from compas_rui.values import BoolValue
from compas_rui.values import FloatValue
from compas_rui.values import IntValue
from compas_rui.values import Settings

SETTINGS = {
    "FormFinder": Settings(
        {
            "autosave.events": BoolValue(True),
            "autoupdate.constraints": BoolValue(False),
        }
    ),
    "Solvers": Settings(
        {
            "constraints.maxiter": IntValue(100),
        }
    ),
}
