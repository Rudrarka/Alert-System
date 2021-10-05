# from modules import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String

db=SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'comment': 'User table'
    }

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v1mc())
    email = db.Column(db.String(), unique=True, nullable=True)
    created = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())

    alerts = db.relationship('Alert', back_populates='user')

    def __repr__(self):
        return f"User('{self.email}')"

class Alert(db.Model):
    __tablename__ = 'alert'
    __table_args__ = (
    db.UniqueConstraint('user_id', 'keyword', name='uq_alert_user_keyword'),
        {
        'comment': 'Alert details'
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v1mc())
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(), unique=False, nullable=False)
    interval = db.Column(db.Integer(), unique=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    updated = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    last_email_sent = db.Column(db.DateTime, nullable=True)
 
    user = db.relationship('User', back_populates='alerts')

    def as_json(self):
        obj = {
            "id": self.id,
            # "user_id": self.user_id,
            "user_email": self.user.email,
            "keyword": self.keyword,
            "interval": self.interval,
            "created": self.created,
            "updated": self.updated
        }

        return obj

class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {
        'comment': 'Product details'
    }

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    product_name = db.Column(db.String(), unique=False, nullable=False)
    price = db.Column(db.Float(), unique=False, nullable=False)
    keywords = db.Column(postgresql.ARRAY(String), unique=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    updated = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
 
    def as_json(self):
        obj = {
            "id": self.id,
            "product_name": self.product_name,
            "price": self.price,
            "keywords": self.keywords,
            "created": self.created,
            "updated": self.updated
        }

        return obj
