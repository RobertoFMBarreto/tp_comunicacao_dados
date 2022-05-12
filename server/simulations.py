from http.client import OK
from unicodedata import name
from webbrowser import Opera
from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for

from server.models.job import Job

from .models.operation import Operation
from .models.simulation import Simulation
from .models.simulations import Simulations
from .models.user import User
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request
from . import db


simulations = Blueprint('simulations', __name__)


@simulations.route('/', methods=['POST'])
@jwt_required()
def createSimulation():
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    data = request.get_json()
    maquinas = data['maquinas']
    jobs = data['jobs']
    operacoes = data['operacoes']
    print(maquinas, jobs, operacoes)
    sim = Simulation(nMaquinas=maquinas, nJobs=jobs,
                     nOperacoes=operacoes, user_id=uid)
    db.session.add(sim)
    db.session.commit()

    return jsonify(sim=sim.to_dict()) if not request.user_agent.platform else redirect(url_for('simulations.getSimulations'))


@simulations.route('/criarSimulacoes', methods=['GET'])
@jwt_required()
def criarSimulacoes():
    verify_jwt_in_request()
    return render_template('createSimulation.html')


@simulations.route('/', methods=['GET'])
@jwt_required()
def getSimulations():
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    sims = Simulation.query.filter_by(user_id=uid).all()
    return jsonify(simulacoes=[sim.to_dict() for sim in sims]) if not request.user_agent.platform else render_template('listSimulations.html', simulations=sims)


@simulations.route('/<simId>', methods=['DELETE'])
@jwt_required()
def removeSimulation(simId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    if(simId == -1):
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
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    if not Job.query.filter_by(name=jobId, sim_id=simId).first():
        job = Job(name=jobId, sim_id=simId)
        db.session.add(job)
        db.session.commit()

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if job:
        jobOperations = Operation.query.filter_by(job_id=job.id).all()
        if jobOperations or len(jobOperations) > 0:
            if opId in [op.number for op in jobOperations]:
                return "Operacao para job já existente", 400

    machine = request.get_json()['machine']
    duration = request.get_json()['duration']

    op = Operation(number=opId, machine=machine,
                   duration=duration, job_id=job.id)
    db.session.add(op)
    db.session.commit()
    return "OK"


@simulations.route('/<simId>/job/<jobId>/operation/<opId>', methods=['GET'])
@jwt_required()
def getOperation(simId=-1, jobId=-1, opId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if not job:
        return "Job inexistente", 400

    operation = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if not operation:
        return "Operação inexistente", 400

    return jsonify(maquina=operation.to_dict()['machine'], duracao=operation.to_dict()['duration']) if not request.user_agent.platform else render_template('operation.html', operation=operation)


@simulations.route('/<simId>/checkTable', methods=['GET'])
@jwt_required()
def checkTable(simId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    msg, val = sim.checkTable(simId, sim.nJobs, sim.nOperacoes, sim.nMaquinas)
    if val == 400:
        return msg, 400
    else:
        return "OK"


@simulations.route('/<simId>/table', methods=['GET'])
@jwt_required()
def getTable(simId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)
    sim = Simulation.query.filter_by(id=simId).first()
    if not sim:
        return "Simulação inexistente", 400

    msg, val = sim.checkTable(simId, sim.nJobs, sim.nOperacoes, sim.nMaquinas)
    if val == 400:
        return msg, 400

    jobs = Job.query.filter_by(sim_id=simId).all()
    if not jobs or len(jobs) == 0:
        return "Nenhum job encontrado", 400

    table = ''
    for job in jobs:
        table += f'Job {job.name}:'
        for operation in Operation.query.filter_by(job_id=job.id).order_by(Operation.number).all():
            table += f'\t({operation.machine}, {operation.duration})'
        table += '\n'

    f = open(f"server/tables/user_{uid}_sim{simId}_table.txt", "w+")
    f.write(table)
    f.close()
    return send_file(f'./tables/user_{uid}_sim{simId}_table.txt', attachment_filename=f'user_{uid}_sim{simId}_table.txt')


""""""""""""""""""""""""""""""
"""         Parte 3        """
""""""""""""""""""""""""""""""


@simulations.route('/<simId>/job/<jobId>/operation/<opId>/initTime/<initTime>', methods=['POST'])
@jwt_required()
def addOpPlanoProducao(simId=-1, jobId=-1, opId=-1, initTime=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)
    initTime = int(initTime)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    job = Job.query.filter_by(name=jobId, sim_id=simId).first()
    if not job:
        return "Job inexistente", 400

    operation = Operation.query.filter_by(number=opId, job_id=job.id).first()
    if not operation:
        return "Operação inexistente", 400

    msg, val = Simulation.addOpPlanoProducao(
        jobId, opId, job, initTime, operation, sim)
    if val == 400:
        return msg, 400
    else:
        return "OK"


@simulations.route('/<simId>/planoProducao/check', methods=['GET'])
@jwt_required()
def checkPlanoProducao(simId=-1):
    simId = int(simId)
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    val, msg = Simulation.checkPlanoProducao(sim.id)
    if val < 0:
        return msg, 400
    else:
        return "OK"


@simulations.route('/<simId>/planoProducao/maxTime', methods=['GET'])
@jwt_required()
def getMaxTimeJobDuration(simId=-1):
    simId = int(simId)
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    maxTime = Simulation.getMaxTimeJobDuration(
        Job.query.filter_by(sim_id=sim.id).all())
    if maxTime['job'] == -1:
        return "Nenhum job encontrado", 400
    else:
        return jsonify(maxTime)


@simulations.route('/<simId>/planoProducao', methods=['GET'])
@jwt_required()
def getPlanoProducao(simId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    path = Simulation.getPlanoProducao(
        Job.query.filter_by(sim_id=sim.id).all())

    return send_file(path, attachment_filename=f'user_{uid}_sim{simId}_planoProducao.txt')


@simulations.route('/<simId>/planoProducao/solve', methods=['GET'])
@jwt_required()
def solvePlanoProducao(simId=-1):
    verify_jwt_in_request()
    email = get_jwt()['sub']
    uid = User.query.filter_by(email=email).first().id
    simId = int(simId)

    sim = Simulation.query.filter_by(id=simId, user_id=uid).first()
    if not sim:
        return "Simulação inexistente", 400

    jobs = Job.query.filter_by(sim_id=sim.id).all()

    if Simulation.checkPlanoProducao(sim.id)[0] != -1:
        return "Plano de produção já foi resolvido ou preenchido", 400

    val, msg = Simulation.solvePlanoProducao(jobs, sim)
    if val < 0:
        return jsonify({'error': msg}), 400
    else:
        return "OK"
