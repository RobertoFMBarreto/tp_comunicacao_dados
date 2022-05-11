
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# Change this!


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'fc9d2e96-2ec3-41dc-b029-e3a93e54cbdb'
    app.config["JWT_SECRET_KEY"] = "6c50fe66-9de0-49bc-8940-a0e39b709155"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    jwt = JWTManager(app)
    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .simulations import simulations as simulations_blueprint
    app.register_blueprint(simulations_blueprint, url_prefix='/simulations')

    return app
