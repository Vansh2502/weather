from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import requests

app = Flask(__name__)

WEATHER_API_KEY = "077268842d79e3d57b43584d36523bbb"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "vansh123",
    "database": "vansh"
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s",
                (username,)
            )

            if cursor.fetchone():
                cursor.close()
                conn.close()
                return "Username already exists!"

            cursor.execute(
                "INSERT INTO users(username,password) VALUES(%s,%s)",
                (username, password)
            )

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for("login"))

        except mysql.connector.Error as err:
            return f"Database Error: {err}"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                return redirect(url_for("weather"))
            else:
                return "Invalid Username or Password!"

        except mysql.connector.Error as err:
            return f"Database Error: {err}"

    return render_template("login.html")


@app.route("/weather", methods=["GET", "POST"])
def weather():

    weather_data = None

    if request.method == "POST":

        city = request.form["city"]

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        try:
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
                    "error": "City not found!"
                }

        except Exception:
            weather_data = {
                "error": "Unable to connect to Weather API"
            }

    return render_template(
        "weather.html",
        weather=weather_data
    )


if __name__ == "__main__":
    app.run(debug=True)