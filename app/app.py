import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "customerdb")
DB_USER = os.getenv("DB_USER", "customeruser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "customerpass")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


@app.route("/")
def home():
    return jsonify({
        "application": "Customer Platform",
        "version": APP_VERSION,
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "status": "running"
    })


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return jsonify({
            "status": "healthy",
            "version": APP_VERSION,
            "database": "connected"
        }), 200

    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "version": APP_VERSION,
            "database": "disconnected",
            "error": str(error)
        }), 500


@app.route("/customers")
def customers():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, name, email FROM customers ORDER BY id;"
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "email": row[2]
            }
            for row in rows
        ])

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)