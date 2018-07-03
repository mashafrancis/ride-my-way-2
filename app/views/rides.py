import psycopg2
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.models import dbconn


class Rides(Resource):
    @staticmethod
    def get():
        try:
            connection = dbconn()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM rides")
            result = cursor.fetchall()
            rides = []
            for row in result:
                rides.append({'ride_id': row[0],
                              'origin': row[1],
                              'destination': row[2],
                              'date': row[3],
                              'time': row[4]})
                connection.close()
            return {'rides': rides}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}


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
        connection = dbconn()
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

    @staticmethod
    def post():
        data = Ride.parser.parse_args()
        try:
            connection = dbconn()
            cursor = connection.cursor()

            ride_offer = (data['origin'],
                          data['destination'],
                          data['date'],
                          data['time'])

            cursor.execute("INSERT INTO rides (ride_id, origin, destination, date, time)"
                           "VALUES(DEFAULT, %s, %s, %s, %s)", ride_offer)

            connection.commit()
            connection.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
        return ride_offer, 201

    @staticmethod
    def delete(ride_id):
        connection = dbconn()
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
        connection = dbconn()
        cursor = connection.curssor()

        cursor.execute("UPDATE rides SET origin = %s, destination = %s, date = %s, time = %s WHERE ride_id = %s",
                       (origin, destination, date, time, ride_id))

        connection.commit()
        connection.close()
