from email.message import EmailMessage
from email_utils import build_body
from  smtplib import SMTP
import os
import logging

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

class EmailService:

    def __init__(self):
        self.msg = EmailMessage()

    def configure_email(self, data):
        self.msg['Subject'] = data["subject"]
        self.msg['From'] = EMAIL_ADDRESS
        self.msg['To'] = data["reciever"]
        body = build_body(data)
        self.msg.set_content(body)
        
    def send_mail(self):
        with SMTP('mailhog', 1025) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(self.msg)

class EmailManager:

    def send_email(self, data):
        try:
            email_service = EmailService()
            email_service.configure_email(data)
            email_service.send_mail()
            return True
        except Exception as e:
            logging.error(e.with_traceback)
