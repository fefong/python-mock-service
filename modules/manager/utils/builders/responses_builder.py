from http import HTTPStatus


class ResponseBuilder:

    FAILURE_MESSAGE = "Request processing failure"
    MESSAGE_NOT_FOUND = "Object not founded"

    @staticmethod
    def response_list(items: list):
        data = {
            "data": {
                "items": [item for item in items],
                "total": len(items)
            }
        }
        return data, HTTPStatus.OK

    @staticmethod
    def response_message(message: str, status_code=HTTPStatus.OK, errors: dict = None, metadata: dict = None):
        data = {
            "data": {
                "message": message,
                **({"errors": errors} if errors else {}),
                **({"metadata": metadata} if metadata else {})
            }
        }
        return data, status_code

    @staticmethod
    def response_fail(message: str = FAILURE_MESSAGE, errors: list = None, metadata: dict = None):
        return ResponseBuilder.response_message(message, HTTPStatus.BAD_REQUEST, errors=errors, metadata=metadata)

    @staticmethod
    def response_fail_not_found(message: str = MESSAGE_NOT_FOUND, metadata: dict = None):
        return ResponseBuilder.response_message(message, HTTPStatus.NOT_FOUND, metadata=metadata)
