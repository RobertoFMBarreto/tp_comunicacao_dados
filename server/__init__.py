from datetime import datetime, timezone, timedelta

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token



# Change this!


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'fc9d2e96-2ec3-41dc-b029-e3a93e54cbdb'
    app.config["JWT_SECRET_KEY"] = "6c50fe66-9de0-49bc-8940-a0e39b709155"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    JWTManager(app)
    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1/web')

    from .simulations import simulations as simulations_blueprint
    app.register_blueprint(simulations_blueprint, url_prefix='/api/v1/simulations')

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=1))

            if target_timestamp > exp_timestamp:
                if response.is_json and response.status_code == 200:
                    access_token = create_access_token(identity=get_jwt_identity())
                    d = response.get_json()
                    d['new_token'] = access_token
                    return jsonify(d)

            return response
        except (RuntimeError, KeyError):
            return response

    return app
