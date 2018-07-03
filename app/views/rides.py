from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.models import db


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


class Ride(Resource):
    """
    Contains the method for add, update and deleting a ride
    """
    parser = reqparse.RequestParser()
    parser.add_argument('origin',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('destination',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('date',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('time',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    def get(self, ride_id):
        """
        Get a single ride available
        :param ride_id:
        """
        ride = self.find_by_ride_id(ride_id)
        if ride:
            return ride
        return {'message': 'Ride offer not available'}, 404

    @classmethod
    def find_by_ride_id(cls, ride_id):
        connection = db
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM rides WHERE ride_id = %s", (ride_id,))
        ride = result.fetchone()
        connection.close()

        if ride:
            return {'ride': {'ride_id': ride[0],
                             'origin': ride[1],
                             'destination': ride[2],
                             'date': ride[3],
                             'time': ride[4]}}

    def post(self, ride_id):
        data = Ride.parser.parse_args()

        ride_offer = {'ride_id': ride_id,
                      'origin': data['origin'],
                      'destination': data['destination'],
                      'date': data['date'],
                      'time': data['time']}

        try:
            self.insert(ride_offer)
        except:
            return {'message': 'Sorry, an error occured while editing this ride offer'}

        return ride_offer, 201

    @classmethod
    def insert(cls, ride):
        connection = db
        cursor = connection.cursor()

        ride = (ride['origin'],
                ride['origin'],
                ride['destination'],
                ride['data'],
                ride['time'])

        cursor.execute("INSERT INTO rides (ride_id, origin, destination, date, time)"
                       "VALUES(DEFAULT, %s, %s, %s, %s)", ride)

        connection.commit()
        connection.close()

    def delete(self, ride_id):
        connection = db
        cursor = connection.curssor()

        cursor.execute("DELETE FROM rides WHERE ride_id=%s", (ride_id,))

        connection.commit()
        connection.close()

        return {'message': 'Your ride offer has been removed'}

    def put(self, ride_id):
        data = Ride.parser.parse_args()

        ride = self.find_by_ride_id(ride_id)

        updated_ride = {'ride_id': ride_id,
                        'origin': data['origin'],
                        'destination': data['destination'],
                        'date': data['date'],
                        'time': data['time']}

        if ride is None:
            try:
                self.insert(updated_ride)
            except:
                return {"message": "Error occured while posting your ride offer"}, 500

        else:
            try:
                self.update(updated_ride)
            except:
                return {"message": "Error occured while updating your ride offer"}, 500
            return updated_ride

    @classmethod
    def update(cls, ride_id, origin, destination, date, time):
        connection = db
        cursor = connection.curssor()

        cursor.execute("UPDATE rides SET origin = %s, destination = %s, date = %s, time = %s WHERE ride_id = %s",
                       (origin, destination, date, time, ride_id))

        connection.commit()
        connection.close()
