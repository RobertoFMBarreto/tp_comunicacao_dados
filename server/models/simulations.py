class Simulations:
    simulations = []

    @staticmethod
    def add(simulation):
        Simulations.simulations.append(simulation)

    @staticmethod
    def getSimulations():
        simJson = []
        for sim in Simulations.simulations:
            simJson.append(sim.toJson())
        return simJson

    @staticmethod
    def remove(simId):
        Simulations.simulations = [sim for sim in Simulations.simulations if sim.id != simId]
