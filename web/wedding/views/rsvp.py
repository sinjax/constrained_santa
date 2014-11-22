from flask.ext.mail import Message
from wedding import app,mail
from helpers import *
from wedding.models import *
from flask import request, flash, redirect, url_for, session, render_template, make_response
from IPython import embed

@app.route('/rsvp/confirm/<id>', methods=['GET'])
def rsvpconfirm(id):
    db.session.query(RSVP).filter_by(unique_hash=id).update({"checked":True})
    rsvp = db.session.query(RSVP).filter_by(unique_hash=id).first()
    db.session.commit()
    return "Set %s to checked"%(rsvp.name)
@app.route('/rsvp/deny/<id>', methods=['GET'])
def rsvpdeny(id):
    db.session.query(RSVP).filter_by(unique_hash=id).delete()
    db.session.commit()
    return "Spam Deleted: %s"%(id)
@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    confirmedAttending = db.session.query(RSVP).filter_by(checked=True,attending=True).all()
    if request.method == 'POST':
        attending = False
        errors = dict()
        if invalid(request.form,'name'): 
            errors['name'] = 'Name is required'
        bringingFood = 'bringfood' in request.form
        if (not request.form['email'] or not request.form['phone']) and bringingFood:
            errors['email'] = 'Email or mobile is required if you\'d like to bring food'
            errors['phone'] = 'Email or mobile is required if you\'d like to bring food'
        
        attending = False
        if not 'rsvp' in request.form:
            errors['rsvp'] = 'Please let us know if you will be attending'
        else:
            attending = request.form['rsvp'] == '1'
        request.form.attending = attending
        if attending:
            try:
                if int(request.form['nadults']) < 0:
                    errors['nadults'] = 'Please enter a number'
            except ValueError:
                errors['nadults'] = 'Please enter a number'
            try:
                if int(request.form['nchildren']) < 0:
                    errors['nchildren'] = 'Please enter a number'
            except ValueError:
                errors['nchildren'] = 'Please enter a number'

        if len(errors) == 0:
            try:            
                rsvp = RSVP()
                rsvp.name = request.form['name']
                rsvp.email = request.form['email']
                rsvp.phone = request.form['phone']
                rsvp.attending = attending
                if attending:
                    rsvp.nadults = int(request.form['nadults'])
                    rsvp.nchildren = int(request.form['nchildren'])
                    rsvp.bringingFood = bringingFood
                
                rsvp.comment = request.form['comments']
                db.session.add(rsvp)
                db.session.commit()
                session['rsvp_id'] = rsvp.id

                msg = Message("RSVP submission from: %s"%rsvp.name, recipients=[
                    "emmasinaweddingtime@gmail.com"
                ]
                ,sender="rsvp@emmasinaweddingtime.info"
                ,reply_to=rsvp.email)
                if rsvp.attending:
                    msg.body = render_template('email/rsvp_accept.txt', rsvp=rsvp)
                else:
                    msg.body = render_template('email/rsvp_reject.txt', rsvp=rsvp)
                mail.send(msg)

                return render("rsvp_result.html",form=request.form,errors=errors)
            except Exception, e:
                errors["dberror"] = "Could not create db object: %s"%e
                return render("rsvp.html",errors=errors,form=request.form,confirmedAttending=confirmedAttending)

        else:
            return render("rsvp.html",errors=errors,form=request.form,confirmedAttending=confirmedAttending)
    form = {}
    return render("rsvp.html",form=form,errors={},confirmedAttending=confirmedAttending)

