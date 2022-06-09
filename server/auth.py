from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models.blackList import BlackList
from .models.job import Job
from .models.operation import Operation
from .models.simulation import Simulation
from .models.user import User
from .simulations import isInBlackList

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.get_json()
    email = data['email']
    names = data['name'].split(" ")
    fullName = ''
    for i in range(0, len(names)):
        if i < len(names) - 1:
            fullName += names[i].capitalize() + " "
        else:
            fullName += names[i].capitalize()
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify(msg="Email já existe"), 400

    new_user = User(email=email, name=fullName,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg="OK")


@auth.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return 'Erro! Por favor verifique as suas credenciais e tente denovo.', 400

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    verify_jwt_in_request()

    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401

    db.session.add(BlackList(token=token))
    db.session.commit()
    return "OK"


@auth.route('/info')
@jwt_required()
def getInfo():
    verify_jwt_in_request()
    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401

    email = get_jwt()['sub']
    user = User.query.filter_by(email=email).first()
    return jsonify(user=user.to_dict())


@auth.route('/apagarConta', methods=['DELETE'])
@jwt_required()
def apagarConta():
    verify_jwt_in_request()
    token = request.headers.get("Authorization", "").split()[1]
    if isInBlackList(token):
        return 'Token Inválido', 401

    email = get_jwt()['sub']
    user = User.query.filter_by(email=email).first()

    sims = Simulation.query.filter_by(user_id=user.id).all()
    for sim in sims:
        jobs = Job.query.filter_by(sim_id=sim.id).all()
        for job in jobs:
            operations = Operation.query.filter_by(job_id=job.id).all()
            for operation in operations:
                db.session.delete(operation)
            db.session.delete(job)
        db.session.delete(sim)

    db.session.delete(user)
    db.session.commit()
    return "OK"
