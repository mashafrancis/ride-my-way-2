import psycopg2
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, first_name, last_name, username, email, password, car_plate_number):
        self.id = _id
        self.firstname = first_name
        self.lastname = last_name
        self.username = username
        self.email = email
        self.password = password
        self.car_plate_number = car_plate_number

    @classmethod
    def find_by_username(cls, username):
        connection = psycopg2.connect(dbname='andela',
                                      host='localhost',
                                      user='masha',
                                      password='bhakita')

        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = psycopg2.connect(dbname='andela',
                                      host='localhost',
                                      user='masha',
                                      password='bhakita')

        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE id=%s", (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('car_plate_number',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "Username has already been taken."}, 400

        connection = psycopg2.connect(dbname='andela',
                                      host='localhost',
                                      user='masha',
                                      password='bhakita')

        cursor = connection.cursor()

        app_user = (data['firstname'],
                    data['lastname'],
                    data['username'],
                    data['email'],
                    data['password'],
                    data['car_plate_number'])

        cursor.execute("INSERT INTO users (id, first_name, last_name, username, email, password, car_plate_number)"
                       "VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)", app_user)

        connection.commit()
        connection.close()

        return {"message": "User was created successfully."}, 201
