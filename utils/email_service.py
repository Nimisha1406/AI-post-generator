import random

from flask_mail import Mail, Message

from flask import current_app

mail = Mail()


def generate_otp():

    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):

    message = Message(
        subject="AI Post Generator OTP",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
    )

    message.body = f"""

Hello,

Your AI Post Generator verification OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this, please ignore this email.

"""

    mail.send(message)


def send_reset_password_email(email, otp):

    message = Message(
        subject="AI Post Generator Password Reset",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
    )

    message.body = f"""

Hello,

Your password reset OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this request, please ignore this email.

"""

    mail.send(message)
