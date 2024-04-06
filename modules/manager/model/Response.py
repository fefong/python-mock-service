import uuid
from http import HTTPStatus

from marshmallow import Schema, fields, post_load


class Response:
    def __init__(self, status_code=HTTPStatus.OK, headers=None, cookies=None, body=None, delay: int = 0):
        self.id = str(uuid.uuid4())
        self.status_code: int = status_code
        self.headers: dict = headers
        self.cookies: list[dict] = cookies
        self.body: dict = body
        self.delay: int = delay

    def to_dict(self):
        return vars(self)


class ResponseSchema(Schema):
    id = fields.UUID(dump_only=True)
    status_code: int = fields.Integer(missing=HTTPStatus.OK)
    headers: dict = fields.Dict(required=False, missing={})
    cookies: list[dict] = fields.List(fields.Dict(), missing=[])
    body: dict = fields.Dict(required=False, missing={})
    delay: int = fields.Integer(missing=0)

    @post_load
    def make_instance(self, data, **kwargs):
        return Response(**data)
