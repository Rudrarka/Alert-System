from flask import Flask
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from celery import Celery
from flask_apscheduler import APScheduler
import socketio
from os import getenv
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=getenv("DB_URL")

#For persisting jobs in postgres
# app.config['SCHEDULER_JOBSTORES']={'default': SQLAlchemyJobStore(url=getenv("DB_URL"))}

celery_app = Celery('email_sender_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()

sio = socketio.Client()
# sio_conn = sio.connect("http://0.0.0.0:5001") //Issue with socketio connection 

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

from .models import db

db.init_app(app)
app.app_context().push()
db.create_all()

# migrate = Migrate(app, db, compare_type=True)



from modules.alert.routes import module
from modules.etl.routes import etl_module

app.register_blueprint(module, url_prefix = '/alert')
app.register_blueprint(etl_module, url_prefix = '/etl')
