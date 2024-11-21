from compas_fofin.session import FoFinSession

session = FoFinSession()
session.dump("test_session.json")

session.load("test_session.json")

print(session.settings.solver.kmax)
