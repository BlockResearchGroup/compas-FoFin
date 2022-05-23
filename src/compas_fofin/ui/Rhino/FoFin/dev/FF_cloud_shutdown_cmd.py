from compas_ui.ui import UI


__commandname__ = "FF_cloud_shutdown"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.cloud_shutdown()


if __name__ == "__main__":
    RunCommand(True)
