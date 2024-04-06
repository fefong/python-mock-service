from typing import Optional

from modules.manager.model.Endpoint import Endpoint

# TODO: [repository] change to database
rest_objects: list[Endpoint] = []


def save(endpoint: Endpoint) -> None:
    rest_objects.append(endpoint)


def get_all() -> list[Endpoint]:
    return rest_objects


def update(endpoint_id: str, endpoint_updated: Endpoint) -> Optional[Endpoint]:
    for index, endpoint in enumerate(rest_objects):
        if endpoint.id == endpoint_id:
            endpoint_updated.id = endpoint_id
            rest_objects[index] = endpoint_updated
            return endpoint_updated
    return None


def find_endpoint_by_uri_and_method(uri: str, method: str) -> Optional[Endpoint]:
    for endpoint in rest_objects:
        if uri.endswith(endpoint.request.uri) and method == endpoint.request.method:
            return endpoint
    return None


def find_endpoint_by_endpoint_id(endpoint_id: str) -> Optional[Endpoint]:
    for endpoint in rest_objects:
        if endpoint_id == endpoint.id:
            return endpoint
    return None


def find_endpoints_by_uri(uri: str) -> list[Endpoint]:
    endpoints = []
    for endpoint in rest_objects:
        if uri.endswith(endpoint.request.uri):
            endpoints.append(endpoint)
    return endpoints


def find_endpoints_by_method(method: str) -> list[Endpoint]:
    endpoints = []
    for endpoint in rest_objects:
        if method == endpoint.request.method:
            endpoints.append(endpoint)
    return endpoints


def delete_by_endpoint_id(endpoint_id: str) -> Optional[Endpoint]:
    for index, endpoint in enumerate(rest_objects):
        if endpoint.id == endpoint_id:
            del rest_objects[index]
            return endpoint
    return None
