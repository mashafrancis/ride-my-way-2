import psycopg2
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.models.ride import dbconn, RideModel


class Rides(Resource):
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

    @staticmethod
    def get(ride_id):
        """
        Get a single ride available
        :param ride_id:
        """
        try:
            connection = dbconn()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM rides WHERE ride_id = %s", (ride_id,))

            ride = cursor.fetchone()
            connection.close()

            if not ride:
                return {'Error': 'Ride not found'}, 404
            else:
                return {'ride': {'ride_id': ride[0],
                                 'origin': ride[1],
                                 'destination': ride[2],
                                 'date': ride[3],
                                 'time': ride[4]}}, 200
        except psycopg2.DatabaseError as error:
            return {'Error': str(error)}

    @staticmethod
    @jwt_required
    def post():
        """
        Create a new ride offer for users to request
        :return:
        """
        try:
            data = Rides.parser.parse_args()
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
        return {"Message": "Hooray! Your ride offer was created successfully."}, 201

    @staticmethod
    @jwt_required
    def delete(ride_id):
        try:
            connection = dbconn()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM rides WHERE ride_id=%s", (ride_id,))

            connection.commit()
            connection.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
        return {'Message': 'Sadly, You have removed your ride offer'}, 200

    @classmethod
    def insert(cls, ride):
        connection = dbconn()
        cursor = connection.cursor()

        updated_ride = (['origin'],
                ['destination'],
                ['date'],
                ['time'])

        cursor.execute("INSERT INTO rides VALUES(%s, %s, %s, %s)", (ride,))

        if ride is None:
            try:
                Rides.insert(updated_ride)
            except:
                return {"Message": "An error occured while updating your ride."}, 401
            return updated_ride

    @jwt_required
    def put(self, ride_id):
        data = Rides.parser.parse_args()

        ride = RideModel.find_by_ride_id(ride_id)

        updated_ride = {'ride_id': ride_id,
                        'origin': data['origin'],
                        'destination': data['destination'],
                        'date': data['date'],
                        'time': data['time']}

        if ride is None:
            try:
                Rides.insert(updated_ride)
            except:
                return {"message": "Error occured while posting your ride offer"}, 500

        else:
            try:
                Rides.update(updated_ride)
            except:
                return {"message": "Error occured while updating your ride offer"}, 500
            return updated_ride

    @classmethod
    @jwt_required
    def update(cls, ride_id, origin, destination, date, time):
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("UPDATE rides SET origin = %s, destination = %s, date = %s, time = %s WHERE ride_id = %s",
                       (origin, destination, date, time, ride_id))

        connection.commit()
        connection.close()


class Ride(Resource):
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
            return {'Rides Available': rides}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
