from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    paragraph = db.Column(db.String(2000))
    catagry = db.Column(db.String(200))
    show_para = db.Column(db.Boolean(), unique=False, default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

