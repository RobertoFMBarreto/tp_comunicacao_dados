from server import db
from sqlalchemy_serializer import SerializerMixin


class Job(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    sim_id = db.Column(db.Integer, db.ForeignKey(
        'simulation.id'), nullable=False)
