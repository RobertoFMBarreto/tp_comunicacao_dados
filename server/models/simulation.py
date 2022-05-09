

from asyncio import tasks
from models.operation import Operation
from models.autoPlan import AutoPlan


class Simulation:
    def __init__(self, nMaquinas, nJobs, nOperacoes, numero):
        self.id = numero
        self.nMaquinas = nMaquinas
        self.nJobs = nJobs
        self.nOperacoes = nOperacoes

        self.jobs = {
            x: [Operation(-1, -1) for y in range(0, self.nOperacoes)] for x in range(0, self.nJobs)
        }

    def toJson(self) -> dict:
        return {
            'id': self.id,
            'nMaquinas': self.nMaquinas,
            'nJobs': self.nJobs,
            'nOperacoes': self.nOperacoes
        }

    def addOpJob(self, jobId, opId, operation):
        self.jobs[jobId][opId] = operation

    def getOpJob(self, jobId, opId):
        if jobId in self.jobs:
            if opId < len(self.jobs[jobId]):
                operation = self.jobs[jobId][opId]
                return 1, f"(M{operation.machine}, {operation.duration})"
            else:
                return -1, f"Erro, a operacao {opId} nao existe"
        else:
            return -1, f"Erro, o Job {jobId} nao existe"

    def checkTable(self):
        # verificar se todos os jobs foram criados
        if self.nJobs != len(self.jobs):
            jobsNumbers = [x for x in range(0, self.nJobs)]
            jobsEmFalta = [x for x in jobsNumbers if x not in self.jobs.keys()]
            if len(jobsEmFalta) > 0:
                if len(jobsEmFalta) > 1:
                    return -1, f"Os jobs {jobsEmFalta} estão em falta"
                else:
                    return -1, f"O job {jobsEmFalta[0]} está em falta"

        # verificar se todas as operações foram criadas
        for jobId, operacoes in self.jobs.items():
            operationsNumbers = [x for x in range(0, self.nOperacoes)]
            operationsIds = [i for i in range(
                0, len(operacoes)) if operacoes[i].machine != -1]
            operationsEmFalta = list(
                set(operationsNumbers) - set(operationsIds))
            if len(operationsEmFalta) > 0:
                if len(operationsEmFalta) > 1:
                    return -1, f"Erro, as operacoes {operationsEmFalta} estao em falta no Job{jobId}"
                else:
                    return -1, f"Erro, a operacao {operationsEmFalta[0]} esta em falta no Job{jobId}"

        # verificar se todas as maquinas foram utilizadas
        for operacoes in self.jobs.values():
            existMachines = [
                operation.machine for operation in operacoes if operation.machine != -1]
            machines = [x for x in range(0, self.nMaquinas)]
            machinesEmFalta = list(set(machines) - set(existMachines))
            if len(machinesEmFalta) > 0:
                if len(machinesEmFalta) > 1:
                    return -1, f"Erro, as maquinas {machinesEmFalta} estao em falta"
                else:
                    return -1, f"Erro, a maquina {machinesEmFalta[0]} esta em falta"

        return 0, "OK"

    # TODO: Após o término, apenas se pode alterar o valor de cada operação, mas não introduzir novos valores.

    def getTable(self):
        table = ''
        for jobId, operations in self.jobs.items():
            table += f'Job {jobId}:'
            for operation in operations:
                table += f'\t({operation.machine}, {operation.duration})'
            table += '\n'

        f = open(f"./tables/sim{self.id}_table.txt", "w+")
        f.write(table)
        f.close()
        return f"./tables/sim{self.id}_table.txt"

    def isMachineBeingUsed(self, machine, initTime, finishTime):
        for jobId, operations in self.jobs.items():
            for i in range(0, len(operations)):
                if operations[i].machine != -1 and operations[i].machine == machine and operations[i].initTime != -1:
                    if initTime >= operations[i].finishTime or finishTime <= operations[i].initTime:
                        pass
                    else:
                        return jobId, i
        return -1, -1

    def isAfterLastOperation(self, initTime, jobId, opId):
        if opId == 0:
            return -1
        for i in reversed(range(opId)):
            previousOperation = self.jobs[jobId][i]
            if previousOperation.initTime != -1:
                if previousOperation.finishTime <= initTime:
                    return -1
                else:
                    return i
        return -1

    def isBeforeNextOperation(self, finishTime, jobId, opId):
        if opId == len(self.jobs[jobId]) - 1:
            return -1

        for i in range(opId + 1, len(self.jobs[jobId])):
            nextOperation = self.jobs[jobId][i]
            if nextOperation.initTime != -1:
                if nextOperation.initTime >= finishTime:
                    return -1
                else:
                    return i
        return -1

    def addOpPlanoProducao(self, jobId, opId, initTime):
        operacao = self.jobs[jobId][opId]

        if self.isAfterLastOperation(initTime, jobId, opId) != -1:
            return -1, f"Erro, a operacao {opId} tem de ser depois da operacao {opId}"
        if self.isBeforeNextOperation(initTime, jobId, opId) != -1:
            return -1, f"Erro, a operacao {opId} tem de ser antes da operacao {opId}"
        else:
            indexJob, indexOp = self.isMachineBeingUsed(
                operacao.machine, initTime, initTime + operacao.duration)
            if indexJob == -1 or indexOp == -1:
                operacao.setInitTime(initTime)
                return 0, "OK"
            else:
                return -1, f"""Erro, a maquina {operacao.machine} esta a ser utilizada no Job {indexJob} na operacao {indexOp} e apenas termina no tempo {self.jobs[indexJob][indexOp].finishTime}"""

    def checkPlanoProducao(self):
        valuesFalta = []
        for jobId, operations in self.jobs.items():
            for i in range(0, len(operations)):
                if operations[i].initTime == -1:
                    valuesFalta.append(f"Job {jobId} - Operacao {i}")

        if len(valuesFalta) > 0:
            msg = 'Erro, as operacoes:\n'
            for value in valuesFalta:
                msg += f"\t->{value}\n"

            return -1, msg
        else:
            return 0, "OK"

    def getMaxTimeJobDuration(self):
        maxTime = {
            'jobId': -1,
            'time': -1
        }
        for jobId, operations in self.jobs.items():
            if operations[len(operations)-1].finishTime > maxTime['time']:
                maxTime = {'job': jobId,
                           'time': operations[len(operations)-1].finishTime}
        return maxTime

    def getPlanoProducao(self):
        table = ''
        operationsText = {}
        for jobId, operations in self.jobs.items():
            for i in range(0, len(operations)):
                if i in operationsText.keys():
                    operationsText[i] += f'\t({jobId},{i},{operations[i].machine},{operations[i].initTime},{operations[i].duration},{operations[i].finishTime})'
                else:
                    operationsText[i] = f'\t({jobId},{i},{operations[i].machine},{operations[i].initTime},{operations[i].duration},{operations[i].finishTime})'

        for operationId, operation in operationsText.items():
            table += f'Operacao {operationId}:{operation}\n'

        f = open(f"./tables/sim{self.id}_plano_producao.txt", "w+")
        f.write(table)
        f.close()
        return f"./tables/sim{self.id}_plano_producao.txt"

    def solvePlanoProducao(self):
        data = []

        for operations in self.jobs.values():
            task = []
            for operation in operations:
                task.append((operation.machine, operation.duration))

            data.append(task)

        # resolver o plano de producao
        assigned_jobs, all_machines = AutoPlan.solve(data)
        if assigned_jobs == -1 and all_machines == -1:
            return -1, "Erro, nao foi possivel resolver o plano de producao"
        else:
            operationsDict = {}
            for machine in all_machines:
                # Sort by starting time.
                assigned_jobs[machine].sort()
                for assigned_task in assigned_jobs[machine]:
                    if assigned_task.index in operationsDict:
                        operationsDict[assigned_task.index].append({
                            'job': assigned_task.job,
                            'start': assigned_task.start
                        })
                    else:
                        operationsDict[assigned_task.index] = [{
                            'job': assigned_task.job,
                            'start': assigned_task.start
                        }]

            for operationId, operations in operationsDict.items():
                for operation in operations:
                    self.addOpPlanoProducao(
                        operation['job'], operationId, operation['start'])
            return 0, "OK"
