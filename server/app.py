from flask import Flask
from blueprints.simulationsManager import simulations_bp

app = Flask(__name__)

app.register_blueprint(simulations_bp, url_prefix='/simulations/')

app.run()