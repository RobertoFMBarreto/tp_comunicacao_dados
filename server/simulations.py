from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for

from server.models.job import Job
from . import db
from .models.blackList import BlackList

from .models.operation import Operation
from .models.simulation import Simulation
from .models.user import User
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request

simulations = Blueprint('simulations', __name__)


def isInBlackList(token):
    if BlackList.query.filter_by(token=token).first():
        return True
    else:
        return False


@simulations.route('/', methods=['POST'])
@jwt_required()
def createSimulation():
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401

    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    data = request.get_json()
    maquinas = data['maquinas']
    jobs = data['jobs']
    operacoes = data['operacoes']

    sim = Simulation(nMaquinas=maquinas, nJobs=jobs,
                     nOperacoes=operacoes, user_id=uid)
    db.session.add(sim)
    db.session.commit()

    return jsonify(sim=sim.to_dict())


@simulations.route('/', methods=['GET'])
@jwt_required()
def getSimulations():
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    sims = Simulation.query.filter_by(user_id=uid).all()
    return jsonify(simulacoes=[sim.to_dict() for sim in sims])


@simulations.route('/<simId>', methods=['DELETE'])
@jwt_required()
def removeSimulation(simId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    if simId == -1:
        return jsonify({'error': 'Id da simulação inválido'}), 400
    try:
        simId = int(simId)
    except ValueError:
        return jsonify({'error': 'Id da simulação inválido'}), 400

    if not Simulation.query.filter_by(id=simId, user_id=uid).first():
        return jsonify({'error': 'Id da simulação inexistente'}), 400

    Simulation.query.filter_by(id=simId, user_id=uid).delete()
    db.session.commit()
    return redirect(url_for("simulations.getSimulations"))


""""""""""""""""""""""""""""""
"""        Parte 2         """
""""""""""""""""""""""""""""""


@simulations.route('/<simId>/job/<jobId>/operation/<opId>', methods=['POST'])
@jwt_required()
def addnJobs(simId=-1, jobId=-1, opId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    if jobId >= sim.nJobs:
        return jsonify(msg="Job Inválido!"), 400

    if opId >= sim.nOperacoes:
        return jsonify(msg="Operacao Inválida!"), 400

    if Simulation.checkTableCompleted(sim.id, sim.nJobs, sim.nOperacoes, sim.nMaquinas):
        return jsonify(msg="Tabela completa! Impossível adicionar mais operações"), 400

    if not Job.query.filter_by(name=jobId, sim_id=simId).first():
        job = Job(name=jobId, sim_id=simId)
        db.session.add(job)
        db.session.commit()

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    op = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if op:
        return jsonify(msg="Operacao já existente para este job")

    try:
        machine = int(request.get_json()['machine'])
        duration = int(request.get_json()['duration'])
    except ValueError:
        return jsonify(msg="Valores invalidos"), 400

    if machine > sim.nMaquinas:
        return jsonify(msg="Máquina inválida")

    if duration < 1:
        return jsonify(msg="Duracao invalida")

    op = Operation(number=opId, machine=machine,
                   duration=duration, job_id=job.id)
    db.session.add(op)
    db.session.commit()
    return jsonify(msg="Operacao efetuada com sucesso")


@simulations.route('/<simId>/job/<jobId>/operation/<opId>', methods=['PUT'])
@jwt_required()
def editOpJob(simId=-1, jobId=-1, opId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if not job:
        return jsonify(msg="Job inexistente"), 400

    op = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if not op:
        return jsonify(msg="Operacao inexistente para este job")

    try:
        machine = int(request.get_json()['machine'])
        duration = int(request.get_json()['duration'])
    except ValueError:
        return jsonify(msg="Valores invalidos"), 400

    if machine > sim.nMaquinas:
        return jsonify(msg="Maquina invalida")

    if duration < 1:
        return jsonify(msg="Duracao invalida")

    op.machine = machine
    op.duration = duration
    db.session.commit()
    return jsonify(msg="Operacao efetuada com sucesso")


@simulations.route('/<simId>/job/<jobId>/operation/<opId>', methods=['GET'])
@jwt_required()
def getOperation(simId=-1, jobId=-1, opId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if not job:
        return jsonify(msg="Job inexistente"), 400

    operation = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if not operation:
        return jsonify(msg="Operação inexistente"), 400

    return jsonify(maquina=operation.to_dict()['machine'], duracao=operation.to_dict()['duration'])


@simulations.route('/<simId>/checkTable', methods=['GET'])
@jwt_required()
def checkTable(simId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    msg, val = sim.checkTable(simId, sim.nJobs, sim.nOperacoes, sim.nMaquinas)
    if val == 400:
        return jsonify(msg=msg), 400
    else:
        return jsonify(msg="OK")


@simulations.route('/<simId>/table', methods=['GET'])
@jwt_required()
def getTable(simId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    sim = Simulation.query.filter_by(id=simId).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    msg, val = sim.checkTable(simId, sim.nJobs, sim.nOperacoes, sim.nMaquinas)
    if val == 400:
        return jsonify(msg=msg), 400

    jobs = Job.query.filter_by(sim_id=simId).all()
    if not jobs or len(jobs) == 0:
        return jsonify(msg="Nenhum job encontrado"), 400

    table = ''
    for job in jobs:
        table += f'Job {job.name}:'
        for operation in Operation.query.filter_by(job_id=job.id).order_by(Operation.number).all():
            table += f'\t({operation.machine}, {operation.duration})'
        table += '\n'

    f = open(f"server/tables/user_{uid}_sim{simId}_table.txt", "w+")
    f.write(table)
    f.close()
    return send_file(f'./tables/user_{uid}_sim{simId}_table.txt',
                     attachment_filename=f'user_{uid}_sim{simId}_table.txt')


""""""""""""""""""""""""""""""
"""         Parte 3        """
""""""""""""""""""""""""""""""


@simulations.route('/<simId>/job/<jobId>/operation/<opId>/initTime/<initTime>', methods=['POST'])
@jwt_required()
def addOpPlanoProducao(simId=-1, jobId=-1, opId=-1, initTime=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)
    initTime = int(initTime)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if not job:
        return jsonify(msg="Job inexistente"), 400

    operation = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if not operation:
        return jsonify(msg="Operação inexistente"), 400

    msg, val = Simulation.addOpPlanoProducao(
        jobId, opId, job, initTime, operation, sim)
    if val == 400:
        return jsonify(msg=msg), 400
    else:
        return jsonify(msg="OK")


@simulations.route('/<simId>/planoProducao/check', methods=['GET'])
@jwt_required()
def checkPlanoProducao(simId=-1):
    simId = int(simId)
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    val, msg = Simulation.checkPlanoProducao(sim.id)
    if val < 0:
        return jsonify(msg=msg), 400
    else:
        return jsonify(msg="OK")


@simulations.route('/<simId>/planoProducao/maxTime', methods=['GET'])
@jwt_required()
def getMaxTimeJobDuration(simId=-1):
    simId = int(simId)
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    val, msg = Simulation.checkPlanoProducao(sim.id)
    if val < 0:
        return jsonify(msg=msg), 400

    maxTime = Simulation.getMaxTimeJobDuration(
        Job.query.filter_by(sim_id=sim.id).all())
    if maxTime['job'] == -1:
        return jsonify(msg="Nenhum job encontrado"), 400
    else:
        return jsonify(maxTime)


@simulations.route('/<simId>/planoProducao', methods=['GET'])
@jwt_required()
def getPlanoProducao(simId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    val, msg = Simulation.checkPlanoProducao(sim.id)
    if val < 0:
        return jsonify(msg=msg), 400

    path = Simulation.getPlanoProducao(
        Job.query.filter_by(sim_id=sim.id).all())

    return send_file(path, attachment_filename=f'user_{uid}_sim{simId}_planoProducao.txt')


@simulations.route('/<simId>/planoProducao/solve', methods=['GET'])
@jwt_required()
def solvePlanoProducao(simId=-1):
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return jsonify(msg="Simulação inexistente"), 400

    jobs = Job.query.filter_by(sim_id=sim.id).all()

    if Simulation.checkPlanoProducao(sim.id)[0] != -1:
        return jsonify(msg="Plano de produção já foi resolvido ou preenchido"), 400

    val, msg = Simulation.solvePlanoProducao(jobs, sim)
    if val < 0:
        return jsonify({'error': msg}), 400
    else:
        return jsonify(msg="OK")
