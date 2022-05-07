from flask import Blueprint, jsonify, request
from models.simulation import Simulation
from models.simulations import Simulations

simulations_bp = Blueprint('simulations', __name__)

@simulations_bp.route('/', methods=['POST'])
def createSimulation():
    data = request.get_json()
    if 'maquinas' not in data or 'trabalhos' not in data or 'operacoes' not in data:
        return jsonify({'error': 'Missing parameters'}), 400
        
    sim = Simulation(data['maquinas'], data['trabalhos'], data['operacoes'], len(Simulations.simulations))
    Simulations.add(sim)
    return jsonify(sim.toJson())

@simulations_bp.route('/', methods=['GET'])
def getSimulations():
    return jsonify(Simulations.getSimulations())


@simulations_bp.route('/simulation/<simId>', methods=['DELETE'])
def removeSimulation(simId=-1):
  #verificar se foi recebido um id
  if(simId == -1):
    return jsonify({'error': 'Id da simulação inválido'}), 400
  
  #verificar se o id é possivel transformar em int
  try:
    simId=int(simId)
  except ValueError:
    return jsonify({'error': 'Id da simulação inválido'}), 400
  
  #verificar se o id existe
  exists=False
  for sim in Simulations.simulations:
    if sim.id == simId:
      exists=True
      break

  if not exists:
    return jsonify({'error': 'Id da simulação não existe'}), 400


  Simulations.remove(simId)
  return jsonify(Simulations.getSimulations())