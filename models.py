from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CaptionHistory(db.Model):
    __tablename__ = 'caption_history'

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    hashtags = db.Column(db.Text, nullable=True)
    style = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<CaptionHistory id={self.id} style='{self.style}' timestamp={self.timestamp}>"
