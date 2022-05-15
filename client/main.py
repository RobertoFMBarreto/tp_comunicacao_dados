import email
import json
import requests

# criar a simulação


# print(requests.post('http://localhost:5000/api/v1/simulations/',
#       json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)

print(requests.post('http://localhost:5000/api/v1/auth/signup', json={
      'email': 'teste@gmail.com',
      'name': 'teste',
      'password': 'teste'
      }).text)

data = requests.post('http://localhost:5000/api/v1/auth/login', json={
    'email': 'teste@gmail.com',
    'password': 'teste'
}).text
print(data)

token = json.loads(data)['access_token']


print(requests.post('http://localhost:5000/api/v1/simulations/',
      headers={"Authorization": f"Bearer {token}"},
      json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)


print(requests.post('http://localhost:5000/api/v1/simulations/',
      headers={"Authorization": f"Bearer {token}"},
      json={'maquinas': 3, 'jobs': 3, 'operacoes': 3}).text)

# obter as simulações
simulacao = requests.get('http://localhost:5000/api/v1/simulations/',
                         headers={"Authorization": f"Bearer {token}"}).text
print(simulacao)
simulacaoId = json.loads(simulacao)['simulacoes'][0]['id']
simulacaoId1 = json.loads(simulacao)['simulacoes'][len(
    json.loads(simulacao)['simulacoes'])-1]['id']
#
#
# # remover simulação
# # print(requests.delete('http://localhost:5000/api/v1/simulations/17',
# #       headers={"Authorization": f"Bearer {token}"}).text)
#
# # adicionar operação a simulação
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/0',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 0, 'duration': 3}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/1',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 1, 'duration': 2}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/2',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 2, 'duration': 2}).text)
#
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/0',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 0, 'duration': 2}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/2',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 1, 'duration': 4}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/1',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 2, 'duration': 1}).text)
#
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/2',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 0, 'duration': 2}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/0',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 1, 'duration': 4}).text)
# print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/1',
#       headers={"Authorization": f"Bearer {token}"},
#       json={'machine': 2, 'duration': 3}).text)
#
# # get operation
# print(requests.get(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/2',
#       headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # check table
# print(requests.get(f'http://localhost:5000/api/v1/simulations/{simulacaoId}/checkTable',
#       headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # get table
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/table',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # adicionar operação plano produção
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/0/initTime/0',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/2/initTime/5',
#     headers={"Authorization": f"Bearer {token}"}).text)
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/0/operation/1/initTime/3',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/1/initTime/7',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/0/initTime/3',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/1/operation/2/initTime/8',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/0/initTime/13',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/1/initTime/17',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.post(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/job/2/operation/2/initTime/20',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # check table
# print('checkTable: ' + requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/planoProducao/check',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/planoProducao/maxTime',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
#
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId}/planoProducao',
#     headers={"Authorization": f"Bearer {token}"}).text)


print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/0/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 3}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/0/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/0/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 2}).text)

print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/1/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/1/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 4}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/1/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 1}).text)

print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/2/operation/2',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 0, 'duration': 2}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/2/operation/0',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 1, 'duration': 4}).text)
print(requests.post(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/2/operation/1',
      headers={"Authorization": f"Bearer {token}"},
      json={'machine': 2, 'duration': 3}).text)

# # get operation
# print(requests.get(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/job/2/operation/2',
#       headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # check table
# print(requests.get(f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/checkTable',
#       headers={"Authorization": f"Bearer {token}"}).text)
#
#
# # get table
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/table',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# # # solve plano produção
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/planoProducao/solve',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/planoProducao/maxTime',
#     headers={"Authorization": f"Bearer {token}"}).text)
#
# print(requests.get(
#     f'http://localhost:5000/api/v1/simulations/{simulacaoId1}/planoProducao',
#     headers={"Authorization": f"Bearer {token}"}).text)
