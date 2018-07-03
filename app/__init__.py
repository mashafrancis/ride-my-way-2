from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWTError

from app.models import create_tables
from app.views.rides import Ride, Rides
from app.views.users import UserRegister, UserLogin

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(app_config[config_name])

    # create the tables
    create_tables()

    api = Api(app)
    # Setup of the Api Routing
    api.add_resource(Rides, '/v1/rides/')
    api.add_resource(Ride, '/v1/rides/<ride_id>')
    api.add_resource(UserRegister, '/v1/auth/signup')
    api.add_resource(UserLogin, '/v1/auth/login')

    @app.errorhandler(JWTError)
    def auth_error_handler(err):
        return jsonify({'message': 'Could not authorize.'}, 401)

    if __name__ == '__main__':
        app.run(debug=True)

    return app
