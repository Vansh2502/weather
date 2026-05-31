from flask import render_template, request, redirect, url_for

from models.user_model import (
    create_user,
    user_exists,
    validate_user
)

from config import WEATHER_API_KEY

import requests


def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if user_exists(username):
            return "Username already exists!"

        create_user(username, password)

        return redirect(url_for("login"))

    return render_template("signup.html")


def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = validate_user(username, password)

        if user:
            return redirect(url_for("weather"))

        return "Invalid Username or Password"

    return render_template("login.html")


def weather():

    weather_data = None

    if request.method == "POST":

        city = request.form["city"]

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:

            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }

        else:

            weather_data = {
                "error": "City not found"
            }

    return render_template(
        "weather.html",
        weather=weather_data
    )