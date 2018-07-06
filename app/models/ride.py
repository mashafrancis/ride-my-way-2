import psycopg2

from flask import current_app
from app.models import dbconn, create_tables


class RideModel(object):
    def __init__(self, ride_id, origin, destination, date, time):
        self.ride_id = ride_id
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time
        if current_app.config['TESTING']:
            self.conn = psycopg2.connect(host="localhost", database="test_db", user="postgres", password="admin")

        else:
            self.conn = psycopg2.connect(host="localhost",
                                         database="development", user="postgres", password="admin")

    @staticmethod
    def save_ride():
        create_tables()
        connection = dbconn()
        cursor = connection.cursor()

        ride = (['origin'],
                ['destination'],
                ['date'],
                ['time'])

        cursor.execute("INSERT INTO rides (ride_id, origin, destination, date, time)"
                       "VALUES(DEFAULT, %s, %s, %s, %s)", ride)

        connection.commit()
        connection.close()

    @classmethod
    def find_by_ride_id(cls, ride_id):
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rides WHERE ride_id = %s", (ride_id,))

        ride = cursor.fetchone()
        connection.close()

        if ride:
            return {'ride': {'ride_id': ride[0],
                             'origin': ride[1],
                             'destination': ride[2],
                             'date': ride[3],
                             'time': ride[4]}}

    def json(self):
        return {
            "ride_id": self.ride_id,
            "origin": self.origin,
            "destination": self.destination,
            "date": self.date,
            "time": self.time
        }
