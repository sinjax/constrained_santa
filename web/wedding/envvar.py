import os

DEBUG = os.environ.get('DEBUG', False) == "1"
SECRET_KEY = os.environ.get('SECRECT',"notsecret")
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',"sqlite:///test.db")

MAIL_DEFAULT_SENDER = 'wedding@emmasinaweddingtime.info'
MAIL_SERVER = os.environ.get('MAIL_SERVER',None)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME',None)
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD',None)
MAIL_PORT = 465
MAIL_USE_SSL = True