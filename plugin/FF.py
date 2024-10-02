#! python3
# venv: formfinder
# r: compas>=2.4, compas_dr>=0.3, compas_fd>=0.5, compas_rui>=0.2, compas_session>=0.2

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
