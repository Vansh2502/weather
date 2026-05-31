import mysql.connector

from config import DB_CONFIG


class UserModel:

    @staticmethod
    def connect():

        return mysql.connector.connect(
            **DB_CONFIG
        )

    @staticmethod
    def create(
        username,
        password
    ):

        conn = UserModel.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            VALUES(NULL,%s,%s)
            """,
            (
                username,
                password
            )
        )

        conn.commit()

        cursor.close()

        conn.close()

    @staticmethod
    def exists(
        username
    ):

        conn = UserModel.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=%s
            """,
            (username,)
        )

        result = cursor.fetchone()

        cursor.close()

        conn.close()

        return result

    @staticmethod
    def validate(
        username,
        password
    ):

        conn = UserModel.connect()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=%s
            AND password=%s
            """,
            (
                username,
                password
            )
        )

        result = cursor.fetchone()

        cursor.close()

        conn.close()

        return result