import jsonschema

from modules.manager.model.Endpoint import Endpoint
from modules.manager.model.Request import Request
from modules.manager.repository import rest_repository


def check_endpoint(uri: str, method: str) -> Endpoint:
    endpoint = rest_repository.find_endpoint_by_uri_and_method(uri, method)
    if endpoint:
        return endpoint
    else:
        raise Exception(f"endpoint [{uri}] and method [{method}] not founded")


def valid_headers(header_request: dict, request: Request):
    is_valid_headers = False
    if request.validate_header_key:
        for header in request.headers:
            if header.capitalize() in header_request:
                if request.validate_header_values:
                    if header_request[header.capitalize()] == request.headers[header]:
                        is_valid_headers = True
                    else:
                        return False
                else:
                    is_valid_headers = True
            else:
                return False
    else:
        return True
    return is_valid_headers


def valid_schema(body_request: dict, request: Request):
    if request.validate_schema:
        try:
            jsonschema.validate(body_request, request.body_schema)
            return True
        except Exception as e:
            return False
    else:
        return True


def valid_body(body_request: dict, request: Request):
    is_valid_body = False
    if request.validate_body_key:
        for item in request.body:
            if item in body_request:
                if request.validate_body_values:
                    if body_request[item] == request.body[item]:
                        is_valid_body = True
                    else:
                        return False
                else:
                    is_valid_body = True
            else:
                return False
    else:
        return True
    return is_valid_body
