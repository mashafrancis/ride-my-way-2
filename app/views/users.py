from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from app.models import dbconn


class User(Resource):
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
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
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
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('firstname',
                                 type=str,
                                 required=True,
                                 help='This field cannot be left blank')

        self.parser.add_argument('lastname',
                                 type=str,
                                 required=True,
                                 help='This field cannot be left blank')

        self.parser.add_argument('username',
                                 type=str,
                                 required=True,
                                 help='This field cannot be left blank')

        self.parser.add_argument('email',
                                 type=str,
                                 required=True,
                                 help='This field cannot be left blank')

        self.parser.add_argument('password',
                                 type=str,
                                 required=True,
                                 help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()

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

        return {"message": "User was created successfully."}, 201


