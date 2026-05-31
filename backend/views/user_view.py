from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session
)

import requests
import jwt

from datetime import (
    datetime,
    timedelta
)

from config import (
    SECRET_KEY
)

from backend.models.user_model import (
    UserModel
)

from config import (
    WEATHER_API_KEY
)


def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if UserModel.exists(username):

            return "Username already exists!"

        UserModel.create(
            username,
            password
        )

        return redirect(
            url_for("user.login")
        )

    return render_template(
        "signup.html"
    )


def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = UserModel.validate(
            username,
            password
        )

        if user:

            token = jwt.encode(

                {
                    "username": username,

                    "exp":
                    datetime.utcnow()
                    +
                    timedelta(hours=1)

                },

                SECRET_KEY,

                algorithm="HS256"
            )

            session["token"] = token

            return redirect(
                url_for(
                    "user.weather"
                )
            )

        return "Invalid Login"

    return render_template(
        "login.html"
    )
def weather():

    token = session.get(
        "token"
    )

    if not token:

        return "Unauthorized"

    try:

        jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

    except:

        session.pop(
            "token",
            None
        )

        return "Session Expired"

    weather_data = None

    if request.method == "POST":

        city = request.form["city"]

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
        )

        response = requests.get(
            url
        )

        data = response.json()

        if response.status_code == 200:

            weather_data = {

                "city":
                data["name"],

                "temperature":
                data["main"]["temp"],

                "humidity":
                data["main"]["humidity"],

                "description":
                data["weather"][0]["description"]

            }

        else:

            weather_data = {

                "error":
                "City not found"

            }

    return render_template(
        "weather.html",
        weather=weather_data
    )
def verify_token(token):

    try:

        data=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return data

    except:

        return None