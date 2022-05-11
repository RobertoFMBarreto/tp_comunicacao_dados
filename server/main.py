from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from .models.user import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/welcome')
@jwt_required()
def profile():
    email = get_jwt()['sub']
    user = User.query.filter_by(email=email).first()
    return jsonify({"message": f"Welcome to the API {user.name}!"}) if not request.user_agent.platform else render_template('welcome.html', name=g.user.name)
