from server import db
from sqlalchemy_serializer import SerializerMixin


class Operation(db.Model, SerializerMixin):
    serialize_only = ('id', 'number', 'machine', 'duration', 'initTime', 'job_id')
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    machine = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    initTime = db.Column(db.Integer, nullable=True, default=-1)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    def setInitTime(self, initTime):
        self.initTime = initTime
        self.finishTime = self.initTime + self.duration
