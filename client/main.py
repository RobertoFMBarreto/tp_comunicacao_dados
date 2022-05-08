import json
import requests

# criar a simulação
print(requests.post('http://localhost:5000/simulations/',
      json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)
print(requests.post('http://localhost:5000/simulations/',
      json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)

# obter as simulações
print(requests.get('http://localhost:5000/simulations/').text)

# remover simulação
print(requests.delete('http://localhost:5000/simulations/simulation/1').text)

# adicionar operação a simulação
print(requests.post('http://localhost:5000/simulations/simulation/0/job/0/operation/0',
      json={'machine': 0, 'duration': 10}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/0/operation/1',
      json={'machine': 1, 'duration': 10}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/0/operation/2',
      json={'machine': 2, 'duration': 10}).text)

print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/1',
      json={'machine': 1, 'duration': 10}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/0',
      json={'machine': 0, 'duration': 10}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/2',
                    json={'machine': 2, 'duration': 10}).text)


print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/0',
      json={'machine': 0, 'duration': 10}).text)

print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/2',
      json={'machine': 2, 'duration': 10}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/1',
      json={'machine': 1, 'duration': 10}).text)

# check table
print(requests.get('http://localhost:5000/simulations/simulation/0/checkTable').text)

# get operation
print(requests.get('http://localhost:5000/simulations/simulation/0/job/2/operation/2').text)


# get table
print(requests.get('http://localhost:5000/simulations/simulation/0/table').text)
