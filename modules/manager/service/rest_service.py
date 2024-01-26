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


def get_endpoint_by_public_id(public_id):
    return rest_repository.find_endpoint_by_public_id(public_id)


def update_endpoint():
    # TODO: [service] update endpoint
    logging.debug("not yet developed")
    return None


def delete_endpoint(public_id: str) -> Endpoint:
    endpoint_deleted = rest_repository.delete_by_public_id(public_id)
    if not endpoint_deleted:
        metadata = {
            "public_id": public_id
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
            "public_id": endpoint_found.public_id
        }
        raise ConflictError(name=NamesEnum.ENDPOINT, metadata=metadata)
    rest_repository.save(endpoint)
    return endpoint

