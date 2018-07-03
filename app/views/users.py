from flask_restful import Resource, reqparse
from app.models import dbconn


class User:
    def __init__(self, _id, first_name, last_name, username, email, password):
        self.id = _id
        self.firstname = first_name
        self.lastname = last_name
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = dbconn()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = dbconn()
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

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        connection = dbconn()
        cursor = connection.cursor()

        user_register = (data['firstname'],
                         data['lastname'],
                         data['username'],
                         data['email'],
                         data['password'])

        cursor.execute("INSERT INTO users (id, first_name, last_name, username, email, password)"
                       "VALUES(DEFAULT, %s, %s, %s, %s, %s)", user_register)

        connection.commit()
        connection.close()

        return {"message": "User was created successfully."}, 200


class UserLogin(Resource):
    @staticmethod
    def post():
        connection = dbconn()
        cursor = connection.cursor()

        user_login = (['username'], ['password'])

        cursor.execute("INSERT INTO users (username, password)"
                       "VALUES(%s, %s)", user_login)

        connection.commit()
        connection.close()

        if not username:
            return {"message": "Missing username parameter"}, 400
        if not password:
            return {"message": "Missing password parameter"}, 400
        if username != 'test' or password != 'test':
            return {"message": "Bad username or password"}

        return {"message": "Your have logged in successfully"}, 200
