id = "{18a65b9c-1a08-43ef-a1fd-ef458f0a1fa0}"
version = "0.0.1.0"
title = "FoFin"

packages = ["compas", "compas_rhino", "compas_cloud", "compas_ui", "compas_fd", "compas_fofin"]

settings = {
    "solver": {
        "autorun": True,
        "kmax": 100,
        "damping": 0.1,
        "tol": {
            "residuals": 1e-3,
            "displacements": 1e-3
        },
    },
    "cloud": {}
}
