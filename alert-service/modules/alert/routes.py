from flask import Blueprint, request
from modules import app, scheduler
from flask_cors import CORS, cross_origin
from modules.models import db
from .alert_manager import AlertManager

CORS(app)
module = Blueprint('alert', __name__)

@module.route('/', methods=['GET'])
@cross_origin()
def get_alerts():
    res = AlertManager(db=db, scheduler=scheduler).get_alerts(request)
    return res, 200

@module.route('/<alert_id>', methods=['DELETE'])
@cross_origin()
def delete_alert(alert_id):
    res = AlertManager(db=db, scheduler=scheduler).delete_alert(alert_id)
    return res, 200

@module.route('/<alert_id>', methods=['PATCH'])
@cross_origin()
def update_alert(alert_id):
    alert = AlertManager(db=db, scheduler=scheduler).update_alert(request, alert_id)
    return alert.as_json(), 200

@module.route('/', methods=['POST'])
@cross_origin()
def create_alert():
    alert = AlertManager(db=db, scheduler=scheduler).create_alert(request)
    return alert.as_json(), 201