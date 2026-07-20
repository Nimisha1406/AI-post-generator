from database import db

class ScheduledPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    scheduled_datetime = db.Column(db.DateTime, nullable=False)