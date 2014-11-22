import time
import md5
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from IPython import embed
from flask import render_template_string
from flask.ext.mail import Mail

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__.split('.')[0])
app.config.from_object('wedding.envvar')
mail = Mail(app)

import views