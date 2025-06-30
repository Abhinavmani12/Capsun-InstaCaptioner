from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CaptionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    hashtags = db.Column(db.Text, nullable=False)
    style = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
