import asyncio
import logging

from jsonschema._format import FormatChecker
from jsonschema.validators import Draft7Validator

from modules.manager.model.Endpoint import Endpoint
from modules.manager.model.Request import Request
from modules.manager.repository import rest_repository
from modules.manager.utils.exceptions.exceptions import NotFoundError

MESSAGE_ENDPOINT_NOT_FOUND = "URI and Method not founded"
MAX_DELAY_VALUE = 3


def check_endpoint(uri: str, method: str) -> Endpoint:
    endpoint = rest_repository.find_endpoint_by_uri_and_method(uri, method)
    if endpoint:
        return endpoint
    else:
        metadata = {"uri": uri, "method": method}
        raise NotFoundError(name="endpoint", message=MESSAGE_ENDPOINT_NOT_FOUND, metadata=metadata)


async def check_delay(delay) -> None:
    if delay > 0:
        delay = delay if delay < MAX_DELAY_VALUE else MAX_DELAY_VALUE
        logging.debug(f"Start delay: {delay}s")
        await asyncio.sleep(delay)
        logging.debug(f"Finished delay")


def validate_headers(request: Request, header_request: dict) -> bool:
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


def validate_schema(body_schema: dict, input_json: dict) -> list | None:
    UNKNOWN_ERROR_MESSAGE = "Unknown error in validation"
    try:
        validator = Draft7Validator(body_schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(input_json), key=lambda e: e.path)
        if errors:
            return [{
                "message": error.message,
                "schema_path": f"#/{'/'.join(error.schema_path)}"
            } for error in errors]
        return None
    except Exception as ex:
        logging.error(ex)
        return [UNKNOWN_ERROR_MESSAGE]


def validate_body(request: Request, body_request: dict) -> bool:
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
