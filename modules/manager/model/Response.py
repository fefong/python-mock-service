import uuid
from http import HTTPStatus

from marshmallow import Schema, fields, post_load


class Response:
    def __init__(self, status_code=200, headers=None, cookies=None, body=None):
        self.public_id = str(uuid.uuid4())
        self.status_code: int = status_code
        self.headers: dict = headers
        self.cookies: list[dict] = cookies
        self.body: dict = body

    def to_dict(self):
        return vars(self)


class ResponseSchema(Schema):
    public_id = fields.UUID(dump_only=True)
    status_code: int = fields.Integer(missing=HTTPStatus.OK)
    headers: dict = fields.Dict(required=False, missing={})
    cookies: list[dict] = fields.List(fields.Dict(), missing=[])
    body: dict = fields.Dict(required=False, missing={})

    @post_load
    def make_instance(self, data, **kwargs):
        return Response(**data)
