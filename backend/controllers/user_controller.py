from flask import Blueprint

from backend.views.user_view import (
    signup,
    login,
    weather
)

user_bp = Blueprint(
    "user",
    __name__
)

user_bp.route(
    "/signup",
    methods=["GET", "POST"]
)(signup)

user_bp.route(
    "/login",
    methods=["GET", "POST"]
)(login)

user_bp.route(
    "/weather",
    methods=["GET", "POST"]
)(weather)