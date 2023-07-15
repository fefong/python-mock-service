from modules.manager.model.Endpoint import Endpoint
from modules.manager.repository import rest_repository

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
    return None


def delete_endpoint():
    return None


def list_special_tags() -> list[str]:
    return special_tags


def insert_one(endpoint: Endpoint):
    rest_repository.save(endpoint)
    return endpoint
