from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from .database import db


class CableResistance(db.Model):

    __tablename__ = "CableResistance"
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.String(8))
    conductor_material = db.Column(db.String(2))
    conduit_material = db.Column(db.String(5))
    reactance = db.Column(db.Float(precision='5,3'))
    resistance = db.Column(db.Float(precision='5,3'))

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
