import psycopg2
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse, inputs
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import dbconn


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=inputs.regex(r"(.*\S.*)"),
                        location='json',
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('lastname',
                        type=inputs.regex(r"(.*\S.*)"),
                        location='json',
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('username',
                        type=inputs.regex(r"(.*\S.*)"),
                        location='json',
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('email',
                        required=True,
                        location='json',
                        help='This field cannot be left blank',
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    parser.add_argument('password',
                        type=inputs.regex(r"(.*\S.*)"),
                        location='json',
                        required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()

        try:
            connection = dbconn()
            cursor = connection.cursor()

            firstname = data['firstname'],
            lastname = data['lastname'],
            username = data['username'],
            email = data['email'],
            password = data['password']

            password_hash = generate_password_hash(password)
            data = [firstname, lastname, username, email, password_hash]

            cursor.execute("INSERT INTO users (user_id, firstname, lastname, username, email, password)"
                           "VALUES(DEFAULT, %s, %s, %s, %s, %s)", data)

            connection.commit()
            connection.close()
        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

        return {"Message": "User was created successfully."}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        required=True,
                        location='json',
                        help='This field cannot be left blank',
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    parser.add_argument('password',
                        type=inputs.regex(r"(.*\S.*)"),
                        required=True,
                        location='json',
                        help='This field cannot be left blank')

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        try:
            connection = dbconn()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE email = %s;", ([args['email']]))
        except psycopg2.DatabaseError as error:
            return {'Status': 'Failed', 'Data': error}, 500
        results = cursor.fetchone()

        if not results:
            return {'error': 'Authentication failed user unknown'}

        username = results[3]
        stored_password = results[5]

        if check_password_hash(stored_password, password):
            access_token = create_access_token(email, username)

            return {"Success": "Login successful",
                    "access_token": access_token}

        return {'error': 'Wrong credentials'}, 404
