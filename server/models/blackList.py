from server import db
from sqlalchemy_serializer import SerializerMixin


class BlackList(db.Model, SerializerMixin):
    token = db.Column(db.String(200), primary_key=True)