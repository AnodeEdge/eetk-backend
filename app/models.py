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


class ConduitData(db.Model):

    __tablename__ = "ConduitData"
    id = db.Column(db.Integer(), primary_key=True)
    conduit_type = db.Column(db.String(20))
    trade_size = db.Column(db.String(10))
    area = db.Column(db.Float())
    inner_diameter = db.Column(db.Float())

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


class ConductorData(db.Model):

    __tablename__ = "ConductorData"
    id = db.Column(db.Integer(), primary_key=True)
    conductor_type = db.Column(db.String(30))
    conductor_size = db.Column(db.String(15))
    area = db.Column(db.Float())
    diameter = db.Column(db.Float())

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
