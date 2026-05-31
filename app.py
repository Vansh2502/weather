from flask import Flask

from controllers.user_controller import (
    signup,
    login,
    weather
)

app = Flask(__name__)

app.add_url_rule(
    "/signup",
    "signup",
    signup,
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/login",
    "login",
    login,
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/weather",
    "weather",
    weather,
    methods=["GET", "POST"]
)

if __name__ == "__main__":
    app.run(debug=True)