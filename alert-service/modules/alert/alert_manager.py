import logging
from flask import abort
from sqlalchemy import exc
from modules.models import User, Alert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from modules.scheduler.tasks import scheduledTask, search_products

class AlertManager:

    def __init__(self, db, scheduler):
        self.db = db
        self.scheduler=scheduler

    def create_new_alert(self, user_id, keyword, interval):
        return Alert(
            user_id=user_id,
            keyword=keyword,
            interval=interval
        )

    def create_user(self, email):
        return User(
            email=email
        )

    def validate_not_none(self, args):
        for arg in args:
            print(arg)
            if not arg: return        
        return True

    def create_alert(self, request):
        email = request.json.get('email')
        keyword = request.json.get('keyword')
        interval = request.json.get('interval')

        validated = self.validate_not_none([email,keyword,interval])
        if not validated:
            abort(400, f"All fields are required.")
        try:
            user = self.db.session.query(User).filter(User.email == email.strip()).one_or_none()

            if not user:
                new_user = self.create_user(email.strip())
                self.db.session.add(new_user)
                self.db.session.flush()
                alert = self.create_new_alert(new_user.id, keyword.strip(), interval)
            else:
                alert = self.create_new_alert(user.id, keyword.strip(), interval)

            self.db.session.add(alert)
            self.db.session.commit()
            self.scheduler.add_job(id=f"search_{str(alert.id)}",
                            func=search_products, args=[keyword.strip()])
            self.scheduler.add_job(id=str(alert.id), func=scheduledTask,
                            kwargs=alert.as_json(), trigger='interval', seconds=interval*60)

            return alert
        except IntegrityError as e:
            logging.error(e) 
            abort(400, f"Alert with same keyword already exists.")

    def update_alert(self, request, alert_id):
        updated_keyword = request.json.get('keyword')
        email_sent = request.json.get('email_sent')
        interval = request.json.get('interval')
        try:
            alert = self.db.session.query(Alert).filter(Alert.id==alert_id).one_or_none()

            if not alert:
                abort(404, f"Alert not found.")
            
            if updated_keyword:
                alert.keyword = updated_keyword.strip()
                self.scheduler.add_job(id=f"search_{str(alert.id)}",
                            func=search_products, args=[updated_keyword.strip()])
            
            if interval:
                alert.interval = interval
            
            if email_sent:
                update_time = func.current_timestamp()
                alert.last_email_sent = update_time
            self.db.session.add(alert)
            self.db.session.commit()
            if not email_sent:
                self.scheduler.remove_job(str(alert.id))
                self.scheduler.add_job(id=str(alert.id), func=scheduledTask,
                            kwargs=alert.as_json(), trigger='interval', seconds=alert.interval*60)
            return alert
        except IntegrityError as e:
            logging.error(e)
            abort(400, f"Alert with same keyword exists.")

    def delete_alert(self, alert_id):
        alert = self.db.session.query(Alert).filter(Alert.id==alert_id).one_or_none()
        
        if not alert:
            abort(404)
        
        self.db.session.delete(alert)
        self.db.session.commit()
        self.scheduler.delete_job(alert_id)

        return {"status":"deleted"}

    def get_alerts(self, request):
        email = request.args.get('email')
        if not email:
            abort(400, f"Email is required parameter.")
            
        user = self.db.session.query(User).options(
            joinedload(User.alerts)
        ).filter(
            User.email==email.strip()
        ).one_or_none()

        if user is None:
            abort(404)

        res = {'alerts': [a.as_json() for a in user.alerts]}
        return res