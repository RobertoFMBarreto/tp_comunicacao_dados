import email
import json
import requests

# criar a simulação


# print(requests.post('http://localhost:5000/simulations/',
#       json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)

print(requests.post('http://localhost:5000/signup', json={
      'email': 'teste@gmail.com',
      'name': 'teste',
      'password': 'teste'
      }).text)

data = requests.post('http://localhost:5000/login', json={
    'email': 'teste@gmail.com',
    'password': 'teste'
}).text
print(data)

token = json.loads(data)['access_token']


print(requests.post('http://localhost:5000/simulations/',
      headers={"Authorization": f"Bearer {token}"},
      json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)

# obter as simulações
simulacao = requests.get('http://localhost:5000/simulations/',
                         headers={"Authorization": f"Bearer {token}"}).text
print(simulacao)
simulacaoId = json.loads(simulacao)['simulacoes'][0]['id']


# remover simulação
# print(requests.delete('http://localhost:5000/simulations/17',
#       headers={"Authorization": f"Bearer {token}"}).text)

# adicionar operação a simulação
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/0/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 3}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/0/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/0/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 2}).text)

print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/1/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/1/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 4}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/1/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 1}).text)

print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/2/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/2/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 4}).text)
print(requests.post(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/2/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 3}).text)

# get operation
print(requests.get(f'http://localhost:5000/simulations/simulation/{simulacaoId}/job/2/operation/2',
      headers={"Authorization": f"Bearer {token}"}).text)


# check table
print(requests.get(f'http://localhost:5000/simulations/simulation/{simulacaoId}/checkTable',
      headers={"Authorization": f"Bearer {token}"}).text)


# get table
print(requests.get(
    f'http://localhost:5000/simulations/simulation/{simulacaoId}/table',
    headers={"Authorization": f"Bearer {token}"}).text)


# # adicionar operação plano produção
# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/0/operation/0/initTime/0').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/0/operation/2/initTime/5').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/0/operation/1/initTime/3').text)


# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/1/operation/1/initTime/7').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/1/operation/0/initTime/3').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/1/operation/2/initTime/8').text)


# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/2/operation/0/initTime/13').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/2/operation/1/initTime/17').text)

# print(requests.post(
#     'http://localhost:5000/simulations/simulation/0/job/2/operation/2/initTime/20').text)


# # get table
# print(requests.get(
#     'http://localhost:5000/simulations/simulation/0/planoProducao/check').text)


# print(requests.get(
#     'http://localhost:5000/simulations/simulation/0/planoProducao').text)

# print(requests.get(
#     'http://localhost:5000/simulations//simulation/0/planoProducao/maxTime').text)

# # solve plano produção
# print(requests.get(
#     'http://localhost:5000/simulations/simulation/1/planoProducao/solve').text)

# print(requests.get(
#     'http://localhost:5000/simulations/simulation/1/planoProducao/maxTime').text)

# print(requests.get(
#     'http://localhost:5000/simulations/simulation/1/planoProducao').text)
