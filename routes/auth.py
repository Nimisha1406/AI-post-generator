from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from models.otp import OTP
from models.password_reset import PasswordResetOTP
from utils.security import hash_password, check_password
from utils.email_service import generate_otp
from redis_queue import otp_queue
from workers.otp_worker import send_signup_otp, send_password_reset_otp
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__)


# -----------------------------
# SIGNUP
# -----------------------------
@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered."}), 400

    # Delete previous OTP if it exists
    old_otp = OTP.query.filter_by(email=email).first()

    if old_otp:
        db.session.delete(old_otp)
        db.session.commit()

    otp = generate_otp()

    otp_record = OTP(
        username=username,
        email=email,
        password=hash_password(password),
        otp=otp,
        expiry=datetime.now(timezone.utc) + timedelta(minutes=5),
    )

    db.session.add(otp_record)
    db.session.commit()

    otp_queue.enqueue(send_signup_otp, email, otp)

    return jsonify({"message": "OTP sent successfully."}), 200


# -----------------------------
# VERIFY OTP
# -----------------------------
@auth.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.get_json()

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required."}), 400

    record = OTP.query.filter_by(email=email, otp=otp).first()

    if not record:
        return jsonify({"error": "Invalid OTP."}), 400

    expiry_time = record.expiry.replace(tzinfo=timezone.utc)
    if expiry_time < datetime.now(timezone.utc):

        db.session.delete(record)
        db.session.commit()

        return jsonify({"error": "OTP expired."}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        db.session.delete(record)
        db.session.commit()

        return jsonify({"error": "User already exists."}), 400

    user = User(
        username=record.username,
        email=record.email,
        password=record.password,
        email_verified=True,
    )

    db.session.add(user)
    db.session.delete(record)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    
    response = make_response(jsonify({"message": "Account created successfully"}))
    
    set_access_cookies(response, token)
    
    return response


# -----------------------------
# LOGIN
# -----------------------------
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid email."}), 401

    if not check_password(password, user.password):
        return jsonify({"error": "Incorrect password."}), 401

    token = create_access_token(identity=str(user.id))

    response = make_response(
        jsonify(
            {
                "message": "Login successful.",
                "username": user.username,
                "email": user.email,
            }
        )
    )

    set_access_cookies(response, token)

    return response


# -----------------------------
# FORGOT PASSWORD
# -----------------------------
@auth.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Email not registered."}), 404

    # Remove any previous reset OTP
    old_otp = PasswordResetOTP.query.filter_by(email=email).first()

    if old_otp:
        db.session.delete(old_otp)
        db.session.commit()

    otp = generate_otp()

    reset_record = PasswordResetOTP(
        email=email, otp=otp, expiry=datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    db.session.add(reset_record)
    db.session.commit()

    otp_queue.enqueue(send_password_reset_otp, email, otp)

    return jsonify({"message": "Password reset OTP sent successfully."}), 200


# -----------------------------
# RESET PASSWORD
# -----------------------------
@auth.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    if not email or not otp or not new_password:
        return jsonify({"error": "Email, OTP and new password are required."}), 400

    record = PasswordResetOTP.query.filter_by(email=email, otp=otp).first()

    if not record:
        return jsonify({"error": "Invalid OTP."}), 400

    expiry_time = record.expiry.replace(tzinfo=timezone.utc)

    if expiry_time < datetime.now(timezone.utc):
        db.session.delete(record)
        db.session.commit()

        return jsonify({"error": "OTP expired."}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    user.password = hash_password(new_password)

    db.session.delete(record)

    db.session.commit()

    return jsonify({"message": "Password updated successfully."}), 200


# -----------------------------
# LOGOUT
# -----------------------------

@auth.route("/logout", methods=["GET"])
def logout():

    response = make_response(
        jsonify({
            "message": "Logged out"
        })
    )

    unset_jwt_cookies(response)

    return response




@auth.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error":"User not found"
        }),404


    return jsonify({
        "id":user.id,
        "username":user.username,
        "email":user.email
    })
