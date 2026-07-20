from flask import Blueprint, redirect, request, jsonify
import requests
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    decode_token,
    verify_jwt_in_request,
)
from database import db
from models.linkedin import LinkedInProfile
from urllib.parse import urlencode
from config import Config

linkedin = Blueprint("linkedin", __name__)


# -----------------------------------
# CONNECT LINKEDIN
# -----------------------------------


@linkedin.route("/connect", methods=["GET"])
@jwt_required()
def connect_linkedin():

    token = request.cookies.get("access_token_cookie")

    if not token:
        return jsonify({
            "error": "JWT cookie missing"
        }), 401

    params = {
        "response_type": "code",
        "client_id": Config.LINKEDIN_CLIENT_ID,
        "redirect_uri": Config.LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email w_member_social",
        "state": token,
    }

    linkedin_auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(
        params
    )

    return redirect(linkedin_auth_url)


# -----------------------------------
# CALLBACK
# -----------------------------------


@linkedin.route("/callback", methods=["GET"])
def linkedin_callback():

    code = request.args.get("code")

    if not code:

        return jsonify({"error": "Authorization failed"}), 400

    # Exchange code for token

    token_response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Config.LINKEDIN_REDIRECT_URI,
            "client_id": Config.LINKEDIN_CLIENT_ID,
            "client_secret": Config.LINKEDIN_CLIENT_SECRET,
        },
    )

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    if not access_token:

        return (
            jsonify({"error": "Unable to get access token", "details": token_data}),
            400,
        )

    # Get LinkedIn profile

    headers = {"Authorization": f"Bearer {access_token}"}

    profile_response = requests.get(
        "https://api.linkedin.com/v2/userinfo", headers=headers
    )

    profile = profile_response.json()

    if "sub" not in profile:

        return jsonify({"error": "Unable to fetch profile"}), 400

    jwt_token = request.args.get("state")
    if not jwt_token:
        return jsonify({"error": "Missing OAuth state"}), 401
    try:
        decoded = decode_token(jwt_token)
        user_id = decoded["sub"]
    except Exception as e:
        return jsonify({"error": "Invalid JWT", "details": str(e)}), 401

    # Check existing LinkedIn connection

    existing = LinkedInProfile.query.filter_by(user_id=user_id).first()

    if existing:

        existing.linkedin_id = profile.get("sub")

        existing.first_name = profile.get("given_name")

        existing.last_name = profile.get("family_name")

        existing.email = profile.get("email")

        existing.profile_picture = profile.get("picture")

        existing.access_token = access_token

    else:

        linkedin_profile = LinkedInProfile(
            user_id=int(user_id),
            linkedin_id=profile.get("sub"),
            first_name=profile.get("given_name"),
            last_name=profile.get("family_name"),
            email=profile.get("email"),
            profile_picture=profile.get("picture"),
            access_token=access_token,
        )

        db.session.add(linkedin_profile)

    db.session.commit()

    return redirect("/dashboard?linkedin=success")


# -----------------------------------
# STATUS
# -----------------------------------


@linkedin.route("/status", methods=["GET"])
@jwt_required()
def linkedin_status():

    user_id = get_jwt_identity()

    profile = LinkedInProfile.query.filter_by(user_id=user_id).first()

    if not profile:

        return jsonify({"connected": False})

    return jsonify(
        {
            "connected": True,
            "name": profile.first_name + " " + profile.last_name,
            "email": profile.email,
            "picture": profile.profile_picture,
        }
    )


# -----------------------------------
# DISCONNECT
# -----------------------------------


@linkedin.route("/disconnect", methods=["POST"])
@jwt_required()
def disconnect_linkedin():

    user_id = get_jwt_identity()

    profile = LinkedInProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "LinkedIn account not connected."}), 404

    db.session.delete(profile)

    db.session.commit()

    return jsonify({"message": "LinkedIn disconnected successfully."})
