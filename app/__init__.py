from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.models import create_tables
from app.views.rides import Rides, Ride
from app.views.users import UserRegister, UserLogin
from app.views.requests import Request

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(app_config[config_name])
    # app.config['JWT_AUTH_URL_RULE'] = '/v1/auth/login'
    app.secret_key = 'moonpie'

    # create the tables
    create_tables()

    JWTManager(app)

    api = Api(app)

    # Setup of the Api Routing
    api.add_resource(Ride, '/v1/rides')
    api.add_resource(Rides, '/v1/rides/<int:ride_id>', '/v1/rides')
    api.add_resource(UserRegister, '/v1/auth/signup')
    api.add_resource(Request, '/v1/rides/<int:ride_id>/requests')
    api.add_resource(UserLogin, '/v1/auth/login')

    if __name__ == '__main__':
        app.run(debug=True)

    return app
