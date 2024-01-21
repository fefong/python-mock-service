from http import HTTPStatus

from modules.manager.model.Endpoint import Endpoint
from modules.manager.utils.builders.responses_builder import ResponseBuilder


class EndpointResponseBuilder:

    ENDPOINT_CREATED_MESSAGE = "Endpoint created successfully"

    @staticmethod
    def list_endpoints_success(endpoints):
        endpoints_dict = [endpoint.to_dict() for endpoint in endpoints]
        return ResponseBuilder.response_list(endpoints_dict)

    @staticmethod
    def create_endpoint_success(endpoint: Endpoint = None):
        metadata = None
        if endpoint:
            metadata = {
                "public_id": endpoint.public_id,
                "mock": endpoint.request.uri,
                "method": endpoint.request.method
            }
        return ResponseBuilder.response_message(EndpointResponseBuilder.ENDPOINT_CREATED_MESSAGE,
                                                HTTPStatus.CREATED, metadata=metadata)
