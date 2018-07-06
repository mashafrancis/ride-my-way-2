import psycopg2
from flask_restful import Resource
from app.models import dbconn
from flask_jwt_extended import jwt_required


class Request(Resource):
    @staticmethod
    def post(ride_id):
        try:
            connection = dbconn()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM rides WHERE ride_id = %s", (ride_id,))
            row = cursor.fetchone()

            request_ride = ('request_id,'
                            'ride_id',
                            'user_id',
                            'status')

            if row[0] == ride_id:
                return {'Message': 'You have already requested for this ride'}, 400
            cursor.execute("INSERT INTO requests (request_id, ride_id, user_id, status)"
                           "VALUES(DEFAULT, %s, %s, %s)", request_ride)

            cursor.commit()
            cursor.close()
            return {'Message': 'Your have successfully requested for a ride'}, 200
        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def put(ride_id, request_id, status):
        try:
            connection = dbconn()
            cursor = connection.cursor()
            cursor.execute("UPDATE requests SET status = %s WHERE request_id = %s",
                           ('Accepted', request_id))

            connection.commit()
            cursor.close()

            return {'Message': 'Your request has been accepted'}, 201

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def get(ride_id):
        try:
            connection = dbconn()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM requests WHERE ride_id = %s", (ride_id,))

            rows = cursor.fetchall()
            requests = {}
            num = 1
            for row in rows:
                requests[num] = {
                    'request_id': row[0],
                    'ride_id': row[1],
                    'user_id': row[2],
                    'status': row[3]
                }
                num += 1

            cursor.close()
            connection.close()

            return requests

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

