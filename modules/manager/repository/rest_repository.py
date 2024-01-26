from typing import Optional

from modules.manager.model.Endpoint import Endpoint

# TODO: [repository] change to database
rest_objects: list[Endpoint] = []


def get_all() -> list[Endpoint]:
    return rest_objects


def save(endpoint: Endpoint) -> None:
    rest_objects.append(endpoint)


def update(public_id: str, endpoint_updated: Endpoint) -> str:
    try:
        ...
        return public_id
    except Exception as e:
        raise Exception("Exception update")


def find_endpoint_by_uri_and_method(uri: str, method: str) -> Optional[Endpoint]:
    for endpoint in rest_objects:
        if uri.endswith(endpoint.request.uri) and method == endpoint.request.method:
            return endpoint
    return None


def find_endpoint_by_public_id(public_id: str) -> Optional[Endpoint]:
    for endpoint in rest_objects:
        if public_id == endpoint.public_id:
            return endpoint
    return None
