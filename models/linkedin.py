from database import db

class LinkedInProfile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    linkedin_id = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    profile_picture = db.Column(db.String(500))
    headline = db.Column(db.String(500))
    access_token = db.Column(db.String(1000))