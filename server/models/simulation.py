from .operation import Operation
from .job import Job
from .autoPlan import AutoPlan
from server import db
from sqlalchemy_serializer import SerializerMixin


class Simulation(db.Model, SerializerMixin):
    serialize_only = ('id', 'nMaquinas', 'nJobs', 'nOperacoes', 'user_id')
    id = db.Column(db.Integer, primary_key=True)
    nMaquinas = db.Column(db.Integer, nullable=False)
    nJobs = db.Column(db.Integer, nullable=False)
    nOperacoes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def checkTableCompleted(simId, nJobs, nOperacoes, nMaquinas):
        jobs = Job.query.filter_by(sim_id=simId).all()

        if len(jobs) < nJobs:
            return False

        for job in jobs:
            operacoes = Operation.query.filter_by(job_id=job.id).all()
            if len(operacoes) < nOperacoes:
                return False

            existMachines = [operacao.machine for operacao in operacoes]
            machines = [x for x in range(0, nMaquinas)]
            machinesEmFalta = list(set(machines) - set(existMachines))
            if len(machinesEmFalta) > 0:
                return False

        return True

    @staticmethod
    def checkTable(simId, nJobs, nOperacoes, nMaquinas):
        # verificar se todos os jobs foram criados
        jobs = Job.query.filter_by(sim_id=simId).all()
        if not jobs:
            return "Nenhum job criado", 400

        if nJobs != len(jobs):
            jobsNumbers = [x for x in range(0, nJobs)]
            jobsEmFalta = [x.name for x in jobs if x.name not in jobs.keys()]
            if len(jobsEmFalta) > 0:
                if len(jobsEmFalta) > 1:
                    return f"Os jobs {jobsEmFalta} estão em falta", 400
                else:
                    return f"O job {jobsEmFalta[0]} está em falta", 400

        # verificar se todas as operações foram criadas
        allOperations = []
        for job in jobs:
            operations = Operation.query.filter_by(job_id=job.id).all()
            allOperations.append(operations)
            operationsNumbers = [x for x in range(0, nOperacoes)]
            operationsIds = [
                x.number for x in Operation.query.filter_by(job_id=job.id).all()]
            operationsEmFalta = list(
                set(operationsNumbers) - set(operationsIds))
            if len(operationsEmFalta) > 0:
                if len(operationsEmFalta) > 1:
                    return f"Erro, as operacoes {operationsEmFalta} estao em falta no Job{job.name}", 400
                else:
                    return f"Erro, a operacao {operationsEmFalta[0]} esta em falta no Job{job.name}", 400

        # verificar se todas as maquinas foram utilizadas
        for job in jobs:
            operations = Operation.query.filter_by(job_id=job.id).all()
            existMachines = [
                operation.machine for operation in operations]
            machines = [x for x in range(0, nMaquinas)]
            machinesEmFalta = list(set(machines) - set(existMachines))
            if len(machinesEmFalta) > 0:
                if len(machinesEmFalta) > 1:
                    return f"Erro, as maquinas {machinesEmFalta} estao em falta", 400
                else:
                    return f"Erro, a maquina {machinesEmFalta[0]} esta em falta", 400

        return "OK", 200

    # TODO: Após o término, apenas se pode alterar o valor de cada operação, mas não introduzir novos valores.
    @staticmethod
    def isMachineBeingUsed(jobs, opId, machine, initTime, finishTime):
        for job in jobs:
            operations = Operation.query.filter_by(
                job_id=job.id).order_by(Operation.number).all()
            for i in range(0, len(operations)):
                if operations[i].number != opId and operations[i].machine != -1 and operations[i].machine == machine and \
                        operations[i].initTime != -1:
                    opFinishTime = operations[i].initTime + \
                                   operations[i].duration
                    if initTime >= opFinishTime or finishTime <= operations[i].initTime:
                        pass
                    else:
                        return job.id, i
        return -1, -1

    @staticmethod
    def isAfterLastOperation(initTime, jobId, opId):
        if opId == 0:
            return -1
        operations = Operation.query.filter_by(
            job_id=jobId).order_by(Operation.number).all()
        operations = [x for x in operations if x.number < opId]
        for i in reversed(range(len(operations))):
            previousOperation = operations[i]

            if previousOperation.initTime != -1:
                previousFinishTime = previousOperation.initTime + previousOperation.duration
                if previousFinishTime <= initTime:
                    return -1
                else:
                    return i
        return -1

    @staticmethod
    def isBeforeNextOperation(finishTime, jobId, opId, nOperacoes):
        if opId == nOperacoes - 1:
            return -1

        operations = Operation.query.filter_by(
            job_id=jobId).order_by(Operation.number).all()
        operations = [x for x in operations if x.number > opId]

        for i in range(opId + 1, len(operations)):
            nextOperation = operations[i]
            if nextOperation.initTime != -1:

                if nextOperation.initTime >= finishTime:
                    return -1
                else:
                    return i
        return -1

    @staticmethod
    def checkPlanoProducao(simId):
        jobs = Job.query.filter_by(sim_id=simId).all()
        for job in jobs:

        valuesFalta = []
        for job in jobs:
            operations = Operation.query.filter_by(job_id=job.id).all()
            for op in operations:

            for operation in operations:
                if operation.initTime == -1:
                    valuesFalta.append(
                        f"Job {job.name} - Operacao {operation.number}")

        if len(valuesFalta) > 0:
            msg = 'Erro, operações em falta:\n'
            for value in valuesFalta:
                msg += f"\t->{value}\n"

            return -1, msg
        else:
            return 0, "A tabela encontra-se correta"

    @staticmethod
    def getMaxTimeJobDuration(jobs):
        maxTime = {
            'job': -1,
            'time': -1
        }
        for job in jobs:
            operations = Operation.query.filter_by(
                job_id=job.id).order_by(Operation.number).all()
            duration = operations[len(operations) - 1].duration
            initTime = operations[len(operations) - 1].initTime
            if initTime + duration > maxTime['time']:
                maxTime = {'job': job.name,
                           'time': duration + initTime}
        return maxTime

    @staticmethod
    def getPlanoProducao(jobs):
        basePath = '/mnt/sda5/vscode/Licenciatura/2 ano/2semestre/comunicacao_dados/TP1/server'
        table = ''
        operationsText = {}
        for job in jobs:
            operations = Operation.query.filter_by(
                job_id=job.id).order_by(Operation.number).all()
            for i in range(0, len(operations)):
                if i in operationsText.keys():
                    operationsText[
                        i] += f'\t({job.name},{i},{operations[i].machine},{operations[i].initTime},{operations[i].duration},{operations[i].initTime + operations[i].duration})'
                else:
                    operationsText[
                        i] = f'\t({job.name},{i},{operations[i].machine},{operations[i].initTime},{operations[i].duration},{operations[i].initTime + operations[i].duration})'

        for operationId, operation in operationsText.items():
            table += f'Operacao {operationId}:{operation}\n'

        f = open(basePath + f"/tables/sim{id}_plano_producao.txt", "w+")
        f.write(table)
        f.close()
        return basePath + f"/tables/sim{id}_plano_producao.txt"

    def addOpPlanoProducao(jobId, opId, job, initTime, operation, sim):
        isAfterNextOperation = Simulation.isAfterLastOperation(
            initTime, jobId, opId)
        if isAfterNextOperation != -1:
            return f"Erro, a operacao {opId} tem de ser depois da operacao {isAfterNextOperation}", 400

        isBeforeNextOperation = Simulation.isBeforeNextOperation(
            initTime + operation.duration, job.id, opId, sim.nOperacoes)
        if isBeforeNextOperation != -1:
            return f"Erro, a operacao {opId} tem de ser antes da operacao {isBeforeNextOperation}", 400

        jobs = Job.query.filter_by(sim_id=sim.id).all()
        indexJob, indexOp = Simulation.isMachineBeingUsed(
            jobs, opId, operation.machine, initTime, (initTime + operation.duration))

        if indexJob == -1 or indexOp == -1:
            operation.initTime = initTime
            db.session.commit()
            return "OK", 200
        else:
            job = Job.query.filter_by(id=indexJob, sim_id=sim.id).first()
            op = Operation.query.filter_by(
                number=indexOp, job_id=job.id).first()
            return f"Erro, a maquina {operation.machine} esta a ser utilizada no Job {indexJob} na operacao {indexOp} e apenas termina no tempo {op.initTime + op.duration}", 400

    def solvePlanoProducao(jobs, sim):
        data = []

        for job in jobs:
            task = []
            operations = Operation.query.filter_by(
                job_id=job.id).order_by(Operation.number).all()
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
                    job = Job.query.filter_by(
                        name=operation['job'], sim_id=sim.id).first()
                    op = Operation.query.filter_by(
                        job_id=job.id, number=operationId).first()
                    op.initTime = operation['start']
                    db.session.commit()
            return 0, "OK"
