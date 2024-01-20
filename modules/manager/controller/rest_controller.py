import logging
from http import HTTPStatus

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
    return data, HTTPStatus.OK


@rest_blueprint.route("/create/", methods=["POST"])
def post_endpoint():
    try:
        json_data = request.json
        endpoint: Endpoint = EndpointSchema().load(json_data)
        logging.debug(endpoint.__dict__)
        rest_service.insert_one(endpoint)
        data = {
            "message": "Endpoint created successfully",
            "data": {
                "public_id": endpoint.public_id,
                "mock": endpoint.request.uri,
                "method": endpoint.request.method
            }
        }
        return data, HTTPStatus.CREATED
    except ValidationError as ex:
        return __handle_validation_error__(ex)
    except Exception as e:
        return repr(e), HTTPStatus.BAD_REQUEST


@rest_blueprint.route("/update/<id>/", methods=["PUT"])
def put_endpoint(id=None):
    # TODO: [controller] update endpoint (put)
    logging.info("PUT - Update")
    logging.debug("not yet developed")
    return rest_service.get_endpoints(), HTTPStatus.OK


@rest_blueprint.route("/update/<id>/", methods=["PATCH"])
def patch_endpoint(id=None):
    # TODO: [controller] update endpoint (patch)
    logging.info("PATCH - Update")
    logging.debug("not yet developed")
    return rest_service.get_endpoints(), HTTPStatus.OK


@rest_blueprint.route("/delete/<id>/", methods=["DELETE"])
def delete_endpoint(id=None):
    # TODO: [controller] delete endpoint
    logging.debug("not yet developed")
    return rest_service.get_endpoints(), HTTPStatus.OK


@rest_blueprint.route("/special_tags/", methods=["GET"])
def get_special_tags():
    return rest_service.list_special_tags(), HTTPStatus.OK


def __handle_validation_error__(ex: ValidationError):
    errors = []
    for field, message in ex.messages.items():
        errors.append({"field": field, "message": message})
    return {"message": "validation failure", "errors": errors}, HTTPStatus.BAD_REQUEST
