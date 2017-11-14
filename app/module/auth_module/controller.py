import uuid
from datetime import datetime, timedelta

from flask import jsonify
from flask.blueprints import Blueprint
from flask.globals import request

from app.models.client import Client
from app.models.token import Token
from app import db


auth_module = Blueprint('auth', __name__, url_prefix='/auth')


@auth_module.route('/access_token', methods=['POST'])
def access_token():
    
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if not client_id:
        client_id = request.args.get('client_id')
    if not client_secret:
        client_secret = request.args.get('client_secret')
    
    client = Client.query.filter({'client_id' : client_id, 'client_secret' : client_secret}).first()

    db.session.db.Token.remove({
        'created_time': {'$lt': datetime.now() - timedelta(hours=1)}
    }, safe=True)

    if not client:
        return jsonify(error={'message':'Error validating verfication code'}), 401


    # remove expired token
    db.session.db.Token.remove({
        'created_time': {'$lt': datetime.now() - timedelta(hours=1)}
    }, safe=True)

    # create new token
    token=Token(token=str(uuid.uuid4()), client=client, created_time=datetime.now())

    token.save()

    expired_time = token.created_time + timedelta(hours=1)
    expired_in = (expired_time - datetime.now()).total_seconds()
    return jsonify(access_token=token.token, expired_in=expired_in)

