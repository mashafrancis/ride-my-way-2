from flask import Flask
from flask_restful import Resource, reqparse, Api
from app.models import db

app = Flask(__name__)
app.secret_key = 'moonpie'

api = Api(app)


class Ride(Resource):
    """
    Contains the method for add, update and deleting a ride
    """
    parser = reqparse.RequestParser()
    parser.add_argument('origin')

    def get(self, ride_id):
        """
        Get a single ride available
        :param ride_id:
        """
        ride = self.find_by_ride(ride_id)
        if ride:
            return ride
        return {'message': 'Ride not found'}, 404

    @classmethod
    def find_by_ride(cls, ride_id):
        connection = db
        cursor = connection.cursor()

        query = "SELECT * FROM Rides WHERE ride_id=%s"
        result = cursor.execute(query, (ride_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'ride': {'ride_id': row[0],
                             'username': row[1],
                             'origin': row[2],
                             'destination': row[3],
                             'date': row[4],
                             'time': row[5]}}


class Rides(Resource):
    @staticmethod
    def get():
        connection = db
        cursor = connection.cursor()

        query = "SELECT * FROM rides"
        result = cursor.execute(query)
        rides = []
        for row in result:
            rides.append({'ride_id': row[0],
                          'username': row[1],
                          'origin': row[2],
                          'destination': row[3],
                          'date': row[4],
                          'time': row[5]})
            return {'rides': rides}
