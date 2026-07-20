from database import db

class OTP(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    expiry = db.Column(db.DateTime(timezone=True), nullable=False)