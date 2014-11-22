from flask import render_template

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