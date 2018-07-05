from app.models import dbconn
from flask_restful import reqparse


class RideModel:
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

