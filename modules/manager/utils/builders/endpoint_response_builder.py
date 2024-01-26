from http import HTTPStatus

from modules.manager.model.Endpoint import Endpoint
from modules.manager.utils.builders.responses_builder import ResponseBuilder


class EndpointResponseBuilder:

    @staticmethod
    def list_endpoints_success(endpoints):
        endpoints_dict = [endpoint.to_dict() for endpoint in endpoints]
        return ResponseBuilder.response_list(items=endpoints_dict)

    @staticmethod
    def create_endpoint_success(endpoint: Endpoint = None):
        MESSAGE_ENDPOINT_CREATED = "Endpoint created successfully"
        metadata = None
        if endpoint:
            metadata = {
                "public_id": endpoint.public_id,
                "mock": endpoint.request.uri,
                "method": endpoint.request.method
            }
        return ResponseBuilder.response_message(message=MESSAGE_ENDPOINT_CREATED,
                                                status_code=HTTPStatus.CREATED,
                                                metadata=metadata)
