from flask import Blueprint, flash, redirect, url_for, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from .models.blackList import BlackList
from .models.user import User
from server import db
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
