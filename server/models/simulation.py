
class Simulation:
    def __init__(self, nMaquinas, nJobs, nOperacoes, numero) -> None:
        self.id = numero
        self.nMaquinas = nMaquinas
        self.nJobs = nJobs
        self.nOperacoes = nOperacoes
        self.jobs = {}

    def toJson(self) -> dict:
        return{
            'id': self.id,
            'nMaquinas': self.nMaquinas,
            'nJobs': self.nJobs,
            'nOperacoes': self.nOperacoes
        }

    def addOpJob(self, jobId, opId, operation):

        if jobId not in self.jobs:
            self.jobs[jobId] = {
                opId: operation
            }
        else:
            if opId not in self.jobs[jobId].keys():
                self.jobs[jobId][opId] = operation

    def getOpJob(self, jobId, opId):

        if jobId in self.jobs:
            if opId in self.jobs[jobId]:
                operation = self.jobs[jobId][opId]
                return (1, f"(M{operation.machine}, {operation.duration})")
            else:
                return (-1, f"Erro, a operação {opId} não existe")
        else:
            return (-1, f"Erro, o Job {jobId} não existe")

    def checkTable(self):
        if self.nJobs != len(self.jobs):
            jobsNumbers = [x for x in range(0, self.nJobs)]
            jobsEmFalta = [x for x in jobsNumbers if x not in self.jobs.keys()]
            if len(jobsEmFalta) > 1:
                return (-1, f"Os jobs {jobsEmFalta} estão em falta")
            else:
                return (-1, f"O job {jobsEmFalta[0]} está em falta")

        for operacoes in self.jobs.values():
            if self.nOperacoes != len(operacoes.keys()):
                operationsNumbers = [x for x in range(0, self.nOperacoes)]
                operationsEmFalta = [
                    x for x in operationsNumbers if x not in operacoes.keys()]
                if len(operationsEmFalta) > 1:
                    return (-1, f"Erro, as operações {operationsEmFalta} estão em falta")
                else:
                    return (-1, f"Erro, a operação {operationsEmFalta[0]} está em falta")

        for job in self.jobs.values():
            existMachines = [operation.machine for operation in job.values()]
            machines = [x for x in range(0, self.nMaquinas)]
            machinesEmFalta = list(set(machines) - set(existMachines))
            if len(machinesEmFalta) != 0:
                if len(machinesEmFalta) > 1:
                    return (-1, f"Erro, as máquinas {machinesEmFalta} estão em falta")
                else:
                    return (-1, f"Erro, a máquina {machinesEmFalta[0]} está em falta")

        return (0, "OK")

# TODO: Após o término, apenas se pode alterar o valor de cada operação, mas não introduzir novos valores.

    def getTable(self):
        table = ''
        for jobId, operations in self.jobs.items():
            table += f'Job {jobId}:'
            for opId, operation in operations.items():
                table += f'\t({operation.machine}, {operation.duration})'
            table += '\n'

        f = open(f"./tables/sim{self.id}_table.txt", "w+")
        f.write(table)
        f.close()
        return f"./tables/sim{self.id}_table.txt"
