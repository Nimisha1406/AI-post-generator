from functools import wraps
from flask import redirect
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


def guest_only(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request(
                locations=["cookies"]
            )

            return redirect("/dashboard")

        except Exception:

            return func(*args, **kwargs)

    return wrapper



def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request(
                locations=["cookies"]
            )

        except Exception:

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper