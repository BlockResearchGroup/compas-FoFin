#! python3

from compas_fofin.rhino.forms.about import AboutForm

__commandname__ = "FF_about"


def RunCommand(is_interactive):

    AboutForm().show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
