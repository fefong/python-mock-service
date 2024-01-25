import json
import logging
from http import HTTPMethod

from flask import request, Blueprint, Response
from flask_restful import Api

from modules.manager.utils.builders.responses_builder import ResponseBuilder
from modules.manager.utils.exceptions.exceptions import NotFoundError
from modules.mock.config.mock_routes import MockRoutes
from modules.mock.rest.service import mock_rest_service
from modules.mock.rest.service.mock_rest_service import validate_headers, validate_body, validate_schema

mock_rest_blueprint = Blueprint('mock_rest', __name__, url_prefix=MockRoutes.MOCK_REST_BASE)

api = Api(mock_rest_blueprint)

methods = [HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH,
           HTTPMethod.DELETE, HTTPMethod.HEAD, HTTPMethod.OPTIONS]
MESSAGE_INVALID_HEADER = "Invalid Header"
MESSAGE_INVALID_SCHEMA = "Invalid values for o schema"
MESSAGE_INVALID_BODY = "Invalid Body"
MIMETYPE_JSON = "application/json"


@mock_rest_blueprint.route(MockRoutes.MOCK_GENERIC_URI, methods=methods)
async def rest_generic_method(uri: str):
    try:
        logging.debug({"full path": request.url})
        logging.debug({"base url": f"{request.scheme}://{request.host}"})
        logging.debug({'path': request.path})
        logging.debug({'uri': uri})
        logging.debug({'method': request.method.upper()})
        logging.debug({'headers': dict(request.headers)})
        logging.debug({'query_params': dict(request.args)})
        logging.debug({'params': dict(request.values)})
        logging.debug({'body': request.json})
    except Exception as e:
        logging.debug(e)
        return ResponseBuilder.response_fail()

    try:
        endpoint = mock_rest_service.check_endpoint(request.path, request.method)

        if not validate_headers(endpoint.request, dict(request.headers)):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_HEADER)

        if endpoint.request.validate_schema and (errors := validate_schema(endpoint.request.body_schema, request.json)):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_SCHEMA, errors)

        if not validate_body(endpoint.request, request.json):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_BODY)

        await mock_rest_service.check_delay(endpoint.response.delay)

        response = Response(json.dumps(endpoint.response.body), endpoint.response.status_code, mimetype=MIMETYPE_JSON)
        for header in endpoint.response.headers:
            response.headers[header] = endpoint.response.headers[header]
        return response

    except NotFoundError as e:
        return ResponseBuilder.response_fail_not_found(e.message, e.metadata)

    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail()
