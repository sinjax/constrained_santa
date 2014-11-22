from flask import render_template
from flask import Response
from functools import wraps
from flask import jsonify
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

def validate_token(token, time):
    return md5.md5(secret_key+time).hexdigest() == token

def gen_token():
    ts = str(time.time())
    return ts, md5.md5(secret_key+ts).hexdigest()

def render(template_name, **context):
    context['page'] = template_name
    return render_template(template_name, **context)

def invalid(dic,key):
	return key not in dic or len(dic[key])==0

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/javascript; charset=utf-8')
    return decorated_function

def new_alchemy_encoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and not x.startswith("query")]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return str(obj)
    return AlchemyEncoder

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

