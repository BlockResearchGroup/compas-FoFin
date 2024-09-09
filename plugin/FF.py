#! python3

import compas_fofin
from compas_rui.forms import AboutForm


def RunCommand(is_interactive):

    form = AboutForm(
        title=compas_fofin.title,
        description=compas_fofin.description,
        version=compas_fofin.__version__,
        website=compas_fofin.website,
        copyright=compas_fofin.__copyright__,
        license=compas_fofin.__license__,
    )

    form.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
