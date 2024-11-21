from compas_fofin.settings import FoFinSettings

settings = FoFinSettings()

print(FoFinSettings(**settings.model_dump()))
