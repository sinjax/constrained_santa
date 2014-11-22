from wedding.models import db, BaseFields

class RSVP(BaseFields, db.Model):
    name = db.Column(db.String(255))
    email = db.Column(db.String(512))
    phone = db.Column(db.String(512))
    attending = db.Column(db.Boolean)
    comment = db.Column(db.Text)
    nadults = db.Column(db.Integer)
    nchildren = db.Column(db.Integer)
    bringingFood = db.Column(db.Boolean)
    checked = db.Column(db.Boolean,default=False)