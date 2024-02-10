import uuid
from copy import copy

from marshmallow import Schema, fields, post_load

from modules.manager.model.Request import RequestSchema, Request
from modules.manager.model.Response import ResponseSchema, Response


class Endpoint:

    def __init__(self, request: Request, response: Response):
        self.id = str(uuid.uuid4())
        self.request = request
        self.response = response

    def to_dict(self):
        __dict: Endpoint = copy(self)
        __dict.response = self.response.to_dict()
        __dict.request = self.request.to_dict()
        return vars(__dict)


class EndpointSchema(Schema):
    id = fields.UUID(dump_only=True)
    request = fields.Nested(RequestSchema(), required=True)
    response = fields.Nested(ResponseSchema(), required=True)

    @post_load
    def make_instance(self, data, **kwargs):
        return Endpoint(**data)
