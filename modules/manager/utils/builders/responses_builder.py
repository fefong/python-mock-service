from http import HTTPStatus
from flask import Response as FlaskResponse, json


class ResponseBuilder:

    FAILURE_MESSAGE = "Request processing failure"
    MESSAGE_NOT_FOUND = "Object not founded"

    @staticmethod
    def response_base(data: dict, status_code=HTTPStatus.OK) -> FlaskResponse:
        response = {
            "data": data
        }
        return FlaskResponse(response=json.dumps(response, indent=2),
                             status=status_code, content_type='application/json')

    @staticmethod
    def response_list(items: list):
        data_items = {
            "items": [item for item in items],
            "total": len(items)
        }
        return ResponseBuilder.response_base(data_items)

    @staticmethod
    def response_message(message: str, status_code=HTTPStatus.OK, errors: dict = None,
                         metadata: dict = None) -> FlaskResponse:
        data_message = {
            "message": message,
            **({"errors": errors} if errors else {}),
            **({"metadata": metadata} if metadata else {})
        }
        return ResponseBuilder.response_base(data_message, status_code)

    @staticmethod
    def response_fail(message: str = FAILURE_MESSAGE, errors: list = None, metadata: dict = None) -> FlaskResponse:
        return ResponseBuilder.response_message(message, HTTPStatus.BAD_REQUEST, errors=errors, metadata=metadata)

    @staticmethod
    def response_fail_not_found(message: str = MESSAGE_NOT_FOUND, metadata: dict = None) -> FlaskResponse:
        return ResponseBuilder.response_message(message, HTTPStatus.NOT_FOUND, metadata=metadata)
