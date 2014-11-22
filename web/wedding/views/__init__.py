import rsvp
from wedding import app
from helpers import *
import os

@app.route("/place", methods=["GET"])
def place(): return render("place.html")

@app.route("/", methods=["GET"])
def plan(): return render("plan.html")

@app.route("/dinner", methods=["GET"])
def dinner(): return render("dinner.html")

@app.route("/note", methods=["GET"])
def note(): return render("invnote.html")

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
