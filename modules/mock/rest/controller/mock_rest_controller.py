import asyncio
import json
import logging

import flask
from flask import request, Blueprint
from flask_restful import Api

from modules.mock.rest.service import mock_rest_service

mock_rest_blueprint = Blueprint('mock_rest', __name__, url_prefix="/rest/mock")

api = Api(mock_rest_blueprint)


@mock_rest_blueprint.route('/<path:uri>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])
async def rest_generic_method(uri: str):
    try:
        logging.debug({'path': request.path})
        logging.debug({'uri': uri})
        logging.debug({'method': request.method.upper()})
        logging.debug({'headers': dict(request.headers)})
        logging.debug({'query_params': dict(request.args)})
        logging.debug({'params': dict(request.values)})
        logging.debug({'body': request.json})
    except Exception as e:
        logging.debug(e)
        ...
    try:
        endpoint = mock_rest_service.check_endpoint(request.path, request.method)
        if not mock_rest_service.valid_headers(dict(request.headers), endpoint.request):
            return '{"message": "Invalid Header"}', 400

        if not mock_rest_service.valid_schema(request.json, endpoint.request):
            return '{"message": "Invalid Schema"}', 400

        if not mock_rest_service.valid_body(request.json, endpoint.request):
            return '{"message": "Invalid Body"}', 400

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
    except Exception as e:
        return repr(e), 404
