from flask import Blueprint
from flask.globals import request
from flask.json import jsonify
from app import auth

from flask import Blueprint
from flask.globals import request
from flask.json import jsonify
from app import auth


log_scanner_module = Blueprint('log_scanner', __name__, url_prefix='/log-scanner')


@log_scanner_module.route('/logs', methods=['GET'])
@auth.login_required
def get_logs():
    return jsonify({'result' : 'success'})
