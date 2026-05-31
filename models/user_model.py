import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def create_user(username, password):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(%s,%s)",
        (username, password)
    )

    conn.commit()

    cursor.close()
    conn.close()


def user_exists(username):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def validate_user(username, password):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user