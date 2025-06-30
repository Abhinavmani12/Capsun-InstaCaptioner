from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CaptionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(100))
    caption = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    style = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
