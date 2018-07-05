from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWTError, JWT

from app.models import create_tables
from app.views.rides import Rides, Ride
from app.views.users import UserRegister, User
from app.views.auth import authenticate, identity
from app.views.requests import Request

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(app_config[config_name])
    app.config['JWT_AUTH_URL_RULE'] = '/v1/auth/login'
    app.secret_key = 'moonpie'

    # create the tables
    create_tables()

    api = Api(app)

    # Setup of the Api Routing
    api.add_resource(Ride, '/v1/rides')
    api.add_resource(Rides, '/v1/rides/<int:ride_id>', '/v1/rides')
    api.add_resource(UserRegister, '/v1/auth/signup')
    api.add_resource(Request, '/v1/rides/<int:ride_id>/requests')
    # api.add_resource(User, '/v1/auth/login')

    jwt = JWT(app, authenticate, identity)

    @app.errorhandler(JWTError)
    def auth_error_handler(err):
        return jsonify({'message': 'Could not authorize.'}, 401)

    if __name__ == '__main__':
        app.run(debug=True)

    return app
