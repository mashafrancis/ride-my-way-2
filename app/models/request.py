import psycopg2
from app.models import dbconn


class Requests:
    def __init__(self):
        self.connection = dbconn()
        self.cursor = self.connection.cursor()

    def request_ride(self, ride_id):
        try:
            self.cursor.execute("SELECT ride_id FROM requests WHERE user_id = %(user_id)s",
                                {'user_id': user[0]})

            row = self.cursor.fetchone()

            if row[0] == ride_id:
                return {'Message': 'You have already requested for this ride'}, 400
            self.cursor.execute("INSERT INTO requests (user_id, ride_id) VALUES (%s, %s)",
                                [user[0], ride_id])

            self.cursor.commit()
            self.cursor.close()
            return {'Message': 'Your have successfully requested for a ride'}, 200
        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    def edit_requests(self):
        try:
            self.cursor.execute("UPDATE requests SET status = %(status)s WHERE request_id = %(request_id)s",
                                {'status': data['status'], 'request_id': request_id})

            self.connection.commit()
            self.cursor.close()

            return {'Message': 'Your request has been updated'}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    def fetch_all_requests(self):
        try:
            self.cursor.execute("SELECT * FROM requests WHERE ride_id = %(ride_id)s",
                                {'ride_id': ride_id})

            rows = self.cursor.fetchall()
            requests = {}
            num = 1
            for row in rows:
                requests[num] = {
                    'request_id': row[0],
                    'user_id': row[1],
                    'status': row[2]
                }
                num += 1

            self.cursor.close()
            self.connection.close()

            return requests

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
