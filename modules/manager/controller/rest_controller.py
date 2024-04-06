import logging
from http import HTTPStatus, HTTPMethod

from flask import Blueprint, request
from marshmallow import ValidationError

from modules.manager.config.endpoint_routes import EndpointRoutes as Routes
from modules.manager.model.Endpoint import Endpoint, EndpointSchema
from modules.manager.service import rest_service
from modules.manager.utils.builders.endpoint_response_builder import EndpointResponseBuilder
from modules.manager.utils.builders.responses_builder import ResponseBuilder
from modules.manager.utils.exceptions.exceptions import ConflictError, NotFoundError
from modules.manager.utils.handlers.handlers import Handlers

rest_blueprint = Blueprint("rest", __name__, url_prefix=Routes.ENDPOINT_REST_BASE)

MESSAGE_ENDPOINT_LIST_FAIL = "Failure to list endpoints"
MESSAGE_ENDPOINT_CREATE_FAIL = "Failure to create endpoint"
MESSAGE_ENDPOINT_DELETE_FAIL = "Failure to delete endpoint"


@rest_blueprint.route(Routes.ENDPOINT_LIST, methods=[HTTPMethod.GET])
def get_endpoints():
    try:
        endpoints = rest_service.get_endpoints()
        return EndpointResponseBuilder.list_endpoints_success(endpoints)
    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail(MESSAGE_ENDPOINT_LIST_FAIL)


@rest_blueprint.route(Routes.ENDPOINT_LIST_DETAILS, methods=[HTTPMethod.GET])
def get_endpoint_details(endpoint_id: str):
    try:
        endpoint = rest_service.get_endpoint_by_endpoint_id(endpoint_id)
        return EndpointResponseBuilder.endpoint_details_success(endpoint)
    except NotFoundError as ex:
        return ResponseBuilder.response_fail_not_found(message=ex.message, metadata=ex.metadata)
    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail(MESSAGE_ENDPOINT_LIST_FAIL)


@rest_blueprint.route(Routes.ENDPOINT_CREATE, methods=[HTTPMethod.POST])
def post_endpoint():
    try:
        json_data = request.json
        endpoint: Endpoint = EndpointSchema().load(json_data)
        rest_service.insert_one(endpoint)
        return EndpointResponseBuilder.create_endpoint_success(endpoint)
    except ValidationError as ex:
        return Handlers.handler_validation_error(ex)
    except ConflictError as ex:
        return ResponseBuilder.response_fail_conflict(message=ex.message, metadata=ex.metadata)
    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail(MESSAGE_ENDPOINT_CREATE_FAIL)


@rest_blueprint.route(Routes.ENDPOINT_UPDATE_ID, methods=[HTTPMethod.PUT])
def put_endpoint(endpoint_id: str):
    try:
        json_data = request.json
        endpoint: Endpoint = EndpointSchema().load(json_data)
        rest_service.update_endpoint(endpoint_id, endpoint)
        return EndpointResponseBuilder.update_endpoint_success(endpoint)
    except ValidationError as ex:
        return Handlers.handler_validation_error(ex)
    except NotFoundError as ex:
        return ResponseBuilder.response_fail_not_found(message=ex.message, metadata=ex.metadata)
    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail()


@rest_blueprint.route(Routes.ENDPOINT_UPDATE_ID, methods=[HTTPMethod.PATCH])
def patch_endpoint(endpoint_id=None):
    # TODO: [controller] update endpoint (patch)
    logging.info("PATCH - Update")
    logging.debug("not yet developed")
    return rest_service.get_endpoints(), HTTPStatus.OK


@rest_blueprint.route(Routes.ENDPOINT_DELETE_ID, methods=[HTTPMethod.DELETE])
def delete_endpoint(endpoint_id: str):
    try:
        endpoint_id = rest_service.delete_endpoint(endpoint_id)
        return ResponseBuilder.response_message(endpoint_id)
    except NotFoundError as ex:
        return ResponseBuilder.response_fail_not_found(message=ex.message, metadata=ex.metadata)
    except Exception as ex:
        logging.error(ex.__dict__)
        return ResponseBuilder.response_fail(MESSAGE_ENDPOINT_DELETE_FAIL)


@rest_blueprint.route(Routes.ENDPOINT_SPECIAL_TAGS, methods=[HTTPMethod.GET])
def get_special_tags():
    return rest_service.list_special_tags(), HTTPStatus.OK


