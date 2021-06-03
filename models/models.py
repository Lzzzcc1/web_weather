import time
from models import db

class Everyday(db.Model):
    __tablename__ = 'everyday_weather'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    highest_temperature = db.Column(db.String(10))
    lowest_temperature = db.Column(db.String(10))
    weather = db.Column(db.String(10))
    wind_direction = db.Column(db.String(10))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    city = db.Column(db.String(10))


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    special_city = db.Column(db.String(255))

class History(db.Model):
    __tablename__ = 'history_weather'
    id = db.Column(db.Integer, primary_key=True)
    average_high = db.Column(db.String(16))
    average_low = db.Column(db.String(16))
    highest_temperature = db.Column(db.String(16))
    lowest_temperature = db.Column(db.String(16))
    average_air_quality = db.Column(db.Integer)
    highest_air_quality = db.Column(db.Integer)
    lowest_air_quality = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    city = db.Column(db.String(10))

class Future(db.Model):
    __tablename__ = 'future_weather'
    date = db.Column(db.String(50), primary_key=True)
    highest_temperature = db.Column(db.String(10))
    lowest_temperature = db.Column(db.String(10))
    weather = db.Column(db.String(10))
    humidity = db.Column(db.String(10))
    city = db.Column(db.String(10))
