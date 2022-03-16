from compas.plugins import plugin


@plugin(category='install', tryfirst=True)
def installable_rhino_packages():
    return ['compas', 'compas_rhino', 'compas_ghpython', 'compas_ui', 'compas_fd', 'compas_fofin']
