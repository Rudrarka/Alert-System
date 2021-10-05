import time
from celery import Celery
from celery.utils.log import get_task_logger
from email_service import EmailManager
from rest_utils import AlertApi

logger = get_task_logger(__name__)

app = Celery('task', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
app.conf.worker_prefetch_multiplier = 1

@app.task()
def send_email(**kwargs):
    manager = EmailManager()
    sent = manager.send_email(kwargs)
    if not sent:
        return f"Error in sending email."
    if kwargs["type"] == "alert":
        AlertApi().acknowledge_mail_sent(str(kwargs["trigger_id"]))
    return f"Email sent"
