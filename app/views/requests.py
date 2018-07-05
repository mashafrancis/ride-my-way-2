from flask_restful import Resource, reqparse, request
from app.models.request import Requests
from jsonschema import validate


class Request(Resource):
    @staticmethod
    def post(ride_id):
        response = Requests.edit_requests(ride_id)
        return response

    @staticmethod
    def put(ride_id, request_id):
        request_data = {
            "type": "object",
            "properties": {"status": {"enum": ["accepted", "rejected"]}
            }
        }
        data = request.json
        validate(data, request_data)

    @staticmethod
    def get(ride_id):
        response = Requests.fetch_all_requests(ride_id)
        return response
