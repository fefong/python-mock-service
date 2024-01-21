import asyncio
import json
import logging
from http import HTTPStatus, HTTPMethod

import flask
from flask import request, Blueprint
from flask_restful import Api

from modules.manager.utils.builders.responses_builder import ResponseBuilder
from modules.manager.utils.exceptions.exceptions import NotFoundError
from modules.mock.config.mock_routes import MockRoutes
from modules.mock.rest.service import mock_rest_service

mock_rest_blueprint = Blueprint('mock_rest', __name__, url_prefix=MockRoutes.MOCK_REST_BASE)

api = Api(mock_rest_blueprint)

methods = [HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH,
           HTTPMethod.DELETE, HTTPMethod.HEAD, HTTPMethod.OPTIONS]
MESSAGE_INVALID_HEADER = "Invalid Header"
MESSAGE_INVALID_SCHEMA = "Invalid Schema"
MESSAGE_INVALID_BODY = "Invalid Body"


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

        if not mock_rest_service.valid_headers(dict(request.headers), endpoint.request):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_HEADER)

        if not mock_rest_service.valid_schema(request.json, endpoint.request):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_HEADER)

        if not mock_rest_service.valid_body(request.json, endpoint.request):
            return ResponseBuilder.response_fail(MESSAGE_INVALID_BODY)

        if endpoint.response.delay > 0:
            logging.debug(f"Start delay: {endpoint.response.delay}")
            await asyncio.sleep(endpoint.response.delay)
            logging.debug(f"Finished delay")

        response = flask.Response(json.dumps(endpoint.response.body),
                                  endpoint.response.status_code,
                                  mimetype='application/json')
        for header in endpoint.response.headers:
            response.headers[header] = endpoint.response.headers[header]
        return response

    except NotFoundError as e:
        return ResponseBuilder.response_fail_not_found(e.message, e.metadata)

    except Exception as e:
        logging.debug(e.__dict__)
        return ResponseBuilder.response_fail()
