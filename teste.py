from server.models.user import User
from server.models.simulation import Simulation
from server.models.job import Job
from server.models.operation import Operation
from server import db, create_app
db.create_all(app=create_app())
