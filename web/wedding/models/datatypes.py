from wedding.models import db, BaseFields
from sqlalchemy.orm import relationship, backref

class Constraints(BaseFields, db.Model):
    parent_id = db.Column(db.Integer, db.ForeignKey('santas.id'))
    constrainted_santa_id = db.Column(db.Integer)

class Santatrons(BaseFields, db.Model):
	name = db.Column(db.Unicode(255))
	santas =  relationship("Santas")

class Santas(BaseFields, db.Model):
    name = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode(512))
    parent_id = db.Column(db.Integer, db.ForeignKey('santatrons.id'))
    constraints =  relationship("Constraints")
