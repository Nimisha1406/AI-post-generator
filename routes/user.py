from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

user = Blueprint("user", __name__)

@user.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    current_user = User.query.get(user_id)

    return jsonify(
        {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "verified": current_user.email_verified,
        }
    )
