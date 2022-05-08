from fileinput import filename
from flask import Blueprint, jsonify, request, send_file
from models.operation import Operation
from models.simulation import Simulation
from models.simulations import Simulations

simulations_bp = Blueprint('simulations', __name__)


@simulations_bp.route('/', methods=['POST'])
def createSimulation():
    data = request.get_json()
    if 'maquinas' not in data or 'jobs' not in data or 'operacoes' not in data:
        return jsonify({'error': 'Missing parameters'}), 400
    # TODO: pensar em melhor opção para ids
    sim = Simulation(data['maquinas'], data['jobs'],
                     data['operacoes'], len(Simulations.simulations))
    Simulations.add(sim)
    return jsonify(sim.toJson())


@simulations_bp.route('/', methods=['GET'])
def getSimulations():
    return jsonify(Simulations.getSimulations())


@simulations_bp.route('/simulation/<simId>', methods=['DELETE'])
def removeSimulation(simId=-1):
    # verificar se foi recebido um id
    if(simId == -1):
        return jsonify({'error': 'Id da simulação inválido'}), 400

    # verificar se o id é possivel transformar em int
    try:
        simId = int(simId)
    except ValueError:
        return jsonify({'error': 'Id da simulação inválido'}), 400

    # verificar se o id existe
    exists = False
    for sim in Simulations.simulations:
        if sim.id == simId:
            exists = True
            break

    if not exists:
        return jsonify({'error': 'Id da simulação não existe'}), 400

    Simulations.remove(simId)
    return jsonify(Simulations.getSimulations())


"""""""""""""""""""""""""""""
          Parte 2
"""""""""""""""""""""""""""""


@simulations_bp.route('/simulation/<simId>/job/<jobId>/operation/<opId>', methods=['POST'])
def addnJobs(simId=-1, jobId=-1, opId=-1):
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    for sim in Simulations.simulations:
        if sim.id == simId:
            machine = request.get_json()['machine']
            duration = request.get_json()['duration']
            sim.addOpJob(jobId, opId, Operation(opId, machine, duration))

    return "OK"


@simulations_bp.route('/simulation/<simId>/job/<jobId>/operation/<opId>', methods=['GET'])
def getOperation(simId=-1, jobId=-1, opId=-1):
    simId = int(simId)
    jobId = int(jobId)
    opId = int(opId)

    for sim in Simulations.simulations:
        if sim.id == simId:
            val, msg = sim.getOpJob(jobId, opId)
            if val < 0:
                return jsonify({'error': msg}), 400
            else:
                return jsonify({"msg": msg})


@simulations_bp.route('/simulation/<simId>/checkTable', methods=['GET'])
def checkTable(simId=-1):
    simId = int(simId)
    for sim in Simulations.simulations:
        if sim.id == simId:
            val, msg = sim.checkTable()
            if val < 0:
                return jsonify({'error': msg}), 400
            else:
                return jsonify({'success': msg}), 200


@simulations_bp.route('/simulation/<simId>/table', methods=['GET'])
def getTable(simId=-1):
    simId = int(simId)
    for sim in Simulations.simulations:
        if sim.id == simId:
            return send_file(sim.getTable(), attachment_filename=f'sim{simId}_table.txt')
