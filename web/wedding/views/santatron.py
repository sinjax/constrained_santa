from flask.ext.mail import Message
from wedding import app,mail
from helpers import *
from wedding.models import *
from flask import request, flash, redirect, url_for, session, render_template, make_response
from IPython import embed
import santa.graphsanta as graphsanta

@app.route("/santatrons", methods=["GET"])
@returns_json
def santatrons_list(): 
	all_santatrons = db.session.query(Santatrons).all()
	return json.dumps(all_santatrons, cls=new_alchemy_encoder(), check_circular=False)

@app.route("/santatrons", methods=["POST"])
@returns_json
def santatrons_create():
	santatron = Santatrons()
	santatron.name = request.form['name']
	db.session.add(santatron)
	db.session.commit()
	return json.dumps(santatron, cls=new_alchemy_encoder(), check_circular=False)

@app.route("/santatrons/<santatron_id>", methods=["GET"])
@returns_json
def santatrons_get_santas(santatron_id):
	target = db.session.query(Santatrons)\
				.filter_by(id=santatron_id).first()
	if not target:
		raise InvalidUsage("no target found", status_code=400)
	return json.dumps(
			target, 
			cls=new_alchemy_encoder(), 
			check_circular=False)

@app.route("/santatrons/<santatron_id>", methods=["POST"])
@returns_json
def santatrons_add_santa(santatron_id):
	target = db.session.query(Santatrons)\
				.filter_by(id=santatron_id).first()
	if not target:
		raise InvalidUsage("no target found")
	santa = Santas()
	santa.name = request.form['name']
	santa.email = request.form['email']
	for santa_constrain_id in request.form.getlist("constraint"):
		constraint = Constraints()
		constraint.constrainted_santa_id = santa_constrain_id
		santa.constraints.append(constraint)
	target.santas.append(santa)

	db.session.commit()
	return json.dumps(
			target, 
			cls=new_alchemy_encoder(), 
			check_circular=False)

@app.route("/santatrons/<santatron_id>/<santa_id>", methods=["PUT"])
@returns_json
def santatrons_update_santa(santatron_id,santa_id):
	target = db.session.query(Santatrons)\
				.filter_by(id=santatron_id).first()
	if not target: raise InvalidUsage("no santatron found")
	santa = db.session.query(Santas)\
				.filter_by(id=santa_id).first()
	if not santa or santa not in target.santas: raise InvalidUsage("no santa found in this santatron")

	santa.name = request.form['name']
	santa.email = request.form['email']
	santa.constraints = []
	for santa_constrain_id in request.form.getlist("constraint"):
		constraint = Constraints()
		constraint.constrainted_santa_id = santa_constrain_id
		santa.constraints.append(constraint)
	target.santas.append(santa)

	db.session.commit()
	return json.dumps(
			target, 
			cls=new_alchemy_encoder(), 
			check_circular=False)

@app.route("/santatrons/assign/<santatron_id>", methods=["PUT"])
@returns_json
def santatrons_assign(santatron_id):
	target = db.session.query(Santatrons)\
				.filter_by(id=santatron_id).first()
	if not target: raise InvalidUsage("no santatron found")
	if target.assigned: raise InvalidUsage("santatron already assigned")
	gsantaC = graphsanta.Constraints()
	for santa in target.santas:
		gsantaC.add_constraints(santa.id,[c.constrainted_santa_id for c in santa.constraints])
	allocated = graphsanta.allocate([santa.id for santa in target.santas],gsantaC)

	for sid,aid in allocated.items():
		santa = db.session.query(Santas).filter_by(id=sid).first()
		assigned = db.session.query(Santas).filter_by(id=aid).first()
		santa.assigned_id = assigned.id
	target.assigned = True
	db.session.commit()
	return json.dumps(target,cls=new_alchemy_encoder(), check_circular=False)