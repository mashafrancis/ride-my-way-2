import psycopg2
from app.models import db
from flask import jsonify


class Ride:
    @staticmethod
    def create_ride(ride_id, username, origin, destination, date, time):
        connection = psycopg2.connect()
        cursor = connection.cursor()

        cursor.execute(ride)
        connection.commit()
        connection.close()
        return response(jsonify({"message": "Your ride has been successfully created"}), 201)