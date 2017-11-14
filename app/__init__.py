from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from flask import Flask, render_template
from flask import g
from flask_httpauth import HTTPTokenAuth
from flask_mongoalchemy import MongoAlchemy
#from pymongo import MongoClient

# Define the WSGI app object
app = Flask(__name__, static_url_path='/')

# Configuration
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = MongoAlchemy(app)
app.config["MONGO_DBNAME"] = "log_scanner_mod"

#client = MongoClient('localhost', 27017)
#dataset = client['log_scanner_mod']

# Define the generic authentication handler
auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):

    from app.models.token import Token
    data = Token.query.filter({'token':token}).first()

    if data:
        if data.created_time > datetime.now() - timedelta(days=1):
            g.current_user=data.client
            return True

    return False

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.module.auth_module.controller import auth_module
from app.module.log_scanner_module.controller import log_scanner_module 
app.register_blueprint(auth_module)
app.register_blueprint(log_scanner_module)

