from app.db import db
from werkzeug.security import check_password_hash
from datetime import datetime


# User Table for the Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    cars = db.relationship("Car", backref='merchant', passive_deletes=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Car Table for the Database
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    brand = db.Column(db.String(50))
    color = db.Column(db.String(30))
    engine = db.Column(db.Float)
    car_type = db.Column(db.String(50))


# Rental Table for the Database
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", foreign_keys=[user_id], passive_deletes=True)
    merchant = db.relationship("User", foreign_keys=[merchant_id], passive_deletes=True)
    car = db.relationship("Car", passive_deletes=True)



