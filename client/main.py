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
      json={'machine': 0, 'duration': 3}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/0/operation/1',
      json={'machine': 1, 'duration': 2}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/0/operation/2',
      json={'machine': 2, 'duration': 2}).text)

print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/0',
      json={'machine': 0, 'duration': 2}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/2',
      json={'machine': 1, 'duration': 4}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/1/operation/1',
      json={'machine': 2, 'duration': 1}).text)

print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/2',
      json={'machine': 0, 'duration': 2}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/0',
      json={'machine': 1, 'duration': 4}).text)
print(requests.post('http://localhost:5000/simulations/simulation/0/job/2/operation/1',
      json={'machine': 2, 'duration': 3}).text)

# check table
print(requests.get('http://localhost:5000/simulations/simulation/0/checkTable').text)

# get operation
print(requests.get('http://localhost:5000/simulations/simulation/0/job/2/operation/2').text)


# get table
print(requests.get('http://localhost:5000/simulations/simulation/0/table').text)


# adicionar operação plano produção
print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/0/operation/0/initTime/0').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/0/operation/2/initTime/5').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/0/operation/1/initTime/3').text)


print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/1/operation/1/initTime/7').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/1/operation/0/initTime/3').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/1/operation/2/initTime/8').text)


print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/2/operation/0/initTime/13').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/2/operation/1/initTime/17').text)

print(requests.post(
    'http://localhost:5000/simulations/simulation/0/job/2/operation/2/initTime/20').text)


# get table
print(requests.get(
    'http://localhost:5000/simulations/simulation/0/planoProducao/check').text)


print(requests.get(
    'http://localhost:5000/simulations/simulation/0/planoProducao').text)

print(requests.get(
    'http://localhost:5000/simulations//simulation/0/planoProducao/maxTime').text)
