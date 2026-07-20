from flask import Blueprint, render_template
from middlewares.auth import guest_only, login_required

pages = Blueprint("pages", __name__)


@pages.route("/")
def home():

    return render_template("index.html")


@pages.route("/signup")
@guest_only
def signup_page():

    return render_template("signup.html", authenticated=False)


@pages.route("/verify-otp")
@guest_only
def verify_page():

    return render_template("verify_otp.html", authenticated=False)


@pages.route("/login")
@guest_only
def login_page():

    return render_template("login.html", authenticated=False)


@pages.route("/forgot-password")
@guest_only
def forgot_password_page():

    return render_template("forgot_password.html",authenticated=False)


@pages.route("/reset-password")
@guest_only
def reset_password_page():

    return render_template("reset_password.html",authenticated=False)


@pages.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html", authenticated=True)
