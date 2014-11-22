import sys, os
sys.path.append(os.getcwd())
from wedding.models import db
from wedding import app
from IPython import embed


db.create_all()
app.run(port=7171)
