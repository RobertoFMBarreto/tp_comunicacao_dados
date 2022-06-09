from server import db
from sqlalchemy_serializer import SerializerMixin


class User(SerializerMixin, db.Model):
    serialize_only = ('id', 'email', 'name')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    simulations = db.relationship('Simulation', backref='user', lazy=True)
