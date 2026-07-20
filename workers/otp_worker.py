from utils.email_service import send_otp_email, send_reset_password_email


def send_signup_otp(email, otp):

    from app import app

    with app.app_context():
        send_otp_email(email, otp)


def send_password_reset_otp(email, otp):

    from app import app

    with app.app_context():
        send_reset_password_email(email, otp)
