import rsvp
import santatron
from wedding import app
from helpers import *
from wedding.models import *
from wedding import embed
import os
import json
from flask import request

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
@app.route("/", methods=["GET"])
def index(): return render("index.html")

@app.route("/templated/<path:filename>", methods=["GET"])
def templated(filename):
	staticfile = os.sep.join(["wedding/static",filename])
	if not os.path.exists(staticfile):
		return ""

	content = file(staticfile).read()

	return content

@app.route("/robots.txt", methods=["GET"])
def robots():
	return templated("robots.txt")
