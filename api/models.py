from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Coupons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    couponcode = db.Column(db.String)
    description = db.Column(db.Text)
    merchant = db.Column(db.String)
    title = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    expire_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)

    store = db.relationship('Stores')


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Numeric(7, 4))
    long = db.Column(db.Numeric(7, 4))
    city = db.Column(db.String)
    phone = db.Column(db.String)
    state = db.Column(db.String)
    street = db.Column(db.String)
    zip = db.Column(db.String)
