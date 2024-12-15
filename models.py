from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    teams = db.relationship('Team', backref='organization', lazy=True)
    services = db.relationship('Service', backref='organization', lazy=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    status = db.Column(db.String(64))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    incidents = db.relationship('Incident', backref='service', lazy=True)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    status = db.Column(db.String(64))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
