from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=False)
    description = db.Column(db.String)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
