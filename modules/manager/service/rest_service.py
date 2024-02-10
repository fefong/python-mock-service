import logging

from modules.manager.model.Endpoint import Endpoint
from modules.manager.repository import rest_repository
from modules.manager.utils.enums.names_enum import NamesEnum
from modules.manager.utils.exceptions.exceptions import ConflictError, NotFoundError

special_tags = [
    "{$timestamp$}",
    "{$randomUUID$}",
    "{$randomFullName$}",
    "{$randomNumber$}",
    "{$loremIpsum$}",
    "{$dataRequest$}",
    "{$any$}"
]


def get_endpoints():
    """
    The get_endpoints function returns a list of all the endpoints in the ReST repository.

    :return: A list of all the endpoints in the repository
    """
    return rest_repository.get_all()


def get_endpoint(uri: str, method: str):
    return rest_repository.find_endpoint_by_uri_and_method(uri, method)


def get_endpoint_by_endpoint_id(endpoint_id):
    return rest_repository.find_endpoint_by_endpoint_id(endpoint_id)


def update_endpoint(endpoint_id: str, endpoint: Endpoint) -> str:
    metadata = {
        "id": endpoint_id
    }
    endpoint_saved: Endpoint = rest_repository.find_endpoint_by_endpoint_id(endpoint_id)
    if not endpoint_saved:
        raise NotFoundError(NamesEnum.ENDPOINT, metadata=metadata)

    endpoint_updated: Endpoint = rest_repository.update(endpoint_id, endpoint)
    if not endpoint_updated:
        raise NotFoundError(NamesEnum.ENDPOINT, metadata=metadata)
    return endpoint_id


def delete_endpoint(endpoint_id: str) -> Endpoint:
    endpoint_deleted = rest_repository.delete_by_endpoint_id(endpoint_id)
    if not endpoint_deleted:
        metadata = {
            "id": endpoint_id
        }
        raise NotFoundError(NamesEnum.ENDPOINT, metadata=metadata)
    return endpoint_deleted


def list_special_tags() -> list[str]:
    return special_tags


def insert_one(endpoint: Endpoint) -> Endpoint:
    endpoint_found = rest_repository.find_endpoint_by_uri_and_method(endpoint.request.uri, endpoint.request.method)
    if endpoint_found:
        metadata = {
            "uri": endpoint_found.request.uri,
            "method": endpoint_found.request.method,
            "id": endpoint_found.id
        }
        raise ConflictError(name=NamesEnum.ENDPOINT, metadata=metadata)
    rest_repository.save(endpoint)
    return endpoint

