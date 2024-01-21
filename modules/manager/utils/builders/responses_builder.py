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
    def response_message(message: str, status_code: HTTPStatus = HTTPStatus.OK, metadata: dict = None):
        data = {
            "data": {
                "message": message
            }
        }
        if metadata:
            data["data"].update(metadata)
        return data, status_code

    @staticmethod
    def response_fail(message: str = FAILURE_MESSAGE, metadata: dict = None):
        return ResponseBuilder.response_message(message, HTTPStatus.BAD_REQUEST, metadata)

    @staticmethod
    def response_fail_not_found(message: str = MESSAGE_NOT_FOUND):
        return ResponseBuilder.response_message(message, HTTPStatus.NOT_FOUND)
