import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from modules.manager.model.Endpoint import Endpoint, EndpointSchema
from modules.manager.service import rest_service

rest_blueprint = Blueprint("rest", __name__, url_prefix="/endpoints/rest")


@rest_blueprint.route("/", methods=["GET"])
def get_endpoints():
    endpoints = rest_service.get_endpoints()
    data = {
        "endpoints": [
            {
                "manager": endpoint.to_dict()
            }
            for endpoint in endpoints],
        "total": len(endpoints)
    }
    return data


@rest_blueprint.route("/create/", methods=["POST"])
def post_endpoint():
    try:
        json_data = request.json
        endpoint: Endpoint = EndpointSchema().load(json_data)
        logging.debug(endpoint.__dict__)
        rest_service.insert_one(endpoint)
        data = {"mensagem": "Endpoint criado com sucesso"}
        return data, 201
    except ValidationError as ex:
        return __handle_validation_error__(ex)
    except Exception as e:
        return repr(e), 400


@rest_blueprint.route("/update/<id>/", methods=["PUT"])
def put_endpoint(id=None):
    logging.info("PUT - Update")
    return rest_service.get_endpoints()


@rest_blueprint.route("/update/<id>/", methods=["PATCH"])
def patch_endpoint(id=None):
    logging.info("PATCH - Update")
    return rest_service.get_endpoints()


@rest_blueprint.route("/delete/<id>/", methods=["DELETE"])
def delete_endpoint(id=None):
    return rest_service.get_endpoints()


@rest_blueprint.route("/special_tags/", methods=["GET"])
def get_special_tags():
    return rest_service.list_special_tags()


def __handle_validation_error__(ex: ValidationError):
    errors = []
    for field, message in ex.messages.items():
        errors.append({"field": field, "message": message})
    return {"message": "validation failure", "errors": errors}, 400
