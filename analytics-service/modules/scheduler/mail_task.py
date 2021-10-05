import logging
from modules.models import Alert, db, Product
from modules.utils.rest_utils import AlertApi

def get_app():
    from modules import app
    return app

def get_celery_app():
    from modules import celery_app
    return celery_app

def schedule_mail():
    print("in send mail")
    items = [{
        "product_name": "test mail product",
        "change_percent": -12
    }]
    get_celery_app().send_task(
        'task.send_email', 
        kwargs={
            "trigger_id": "id",
            'reciever': "email@email.com",
            "type": "analytics",
            "subject": "Price change alert",
            "items":items
        })

