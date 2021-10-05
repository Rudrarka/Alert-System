from flask import Flask
from flask_migrate import Migrate
from celery import Celery
from flask_apscheduler import APScheduler
from os import getenv
from .models import db
from .scheduler.etl_task import etl
from .scheduler.mail_task import schedule_mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DB_URL")
app.config['SCHEDULER_API_ENABLED'] = True
celery_app = Celery('email_sender_worker',
                    broker='redis://redis:6379/0', backend='redis://redis:6379/0')
app.config['JOBS'] = [
    {
        "id": "etl_job",
        "func": etl,
        "trigger": "cron",
        "hour": "22",
        "minute":"00",
    },
    {
        "id": "mail_job",
        "func": schedule_mail,
        "trigger": "cron",
        "hour": "23",
        "minute":"00",
    }
]
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
with app.app_context():
    db.init_app(app)
    db.create_all()

# migrate = Migrate(app, db, compare_type=True)
