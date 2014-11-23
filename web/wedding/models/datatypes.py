from wedding.models import db, BaseFields
from sqlalchemy.orm import relationship, backref

class Constraints(BaseFields, db.Model):
    parent_id = db.Column(db.Integer, db.ForeignKey('santas.id'))
    constrainted_santa_id = db.Column(db.Integer)

class Santatrons(BaseFields, db.Model):
	name = db.Column(db.Unicode(255))
	santas =  relationship("Santas")
	assigned = db.Column(db.Boolean(),default=False)

class Santas(BaseFields, db.Model):
    name = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode(512))
    santatron_id = db.Column(db.Integer, db.ForeignKey('santatrons.id'))
    assigned_id = db.Column(db.Integer)
    constraints =  relationship("Constraints")
    confirmed = db.Column(db.Boolean(),default=False)
    # assigned = relationship("Santas",uselist=False)
