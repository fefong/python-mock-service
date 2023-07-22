import uuid
from http import HTTPMethod

from marshmallow import Schema, fields, post_load, ValidationError
from marshmallow_enum import EnumField


class Request:
    def __init__(self, uri: str, method: str,
                 query_params=None, validate_query_params_key=False, validate_query_params_values=False,
                 headers=None, validate_header_key=False, validate_header_values=False,
                 body_schema=None, validate_schema=False,
                 body=None, validate_body_key=False, validate_body_values=False):
        self.public_id = str(uuid.uuid4())
        self.uri: str = uri
        self.method: str = method
        self.query_params: list[str] = query_params
        self.validate_query_params_key: bool = validate_query_params_key
        self.validate_query_params_values: bool = validate_query_params_values
        self.headers: dict = headers
        self.validate_header_key: bool = validate_header_key
        self.validate_header_values: bool = validate_header_values
        self.body_schema: dict = body_schema
        self.validate_schema: bool = validate_schema
        self.body: dict = body
        self.validate_body_key: bool = validate_body_key
        self.validate_body_values: bool = validate_body_values
        self.__validate_flags__()

    def to_dict(self):
        return vars(self)

    def __validate_flags__(self):
        errors = []
        if not self.validate_header_key and self.validate_header_values:
            errors.append({"validate_header_values": "Field 'validate_header_key' must be true"})
        if not self.validate_body_key and self.validate_body_values:
            errors.append({"validate_body_key": "Field 'validate_body_key' must be true"})
        if self.validate_schema and (self.validate_body_key or self.validate_body_values):
            error_schema = []
            if self.validate_body_key:
                error_schema.append("Field 'validate_body_key' must be false")
            if self.validate_body_values:
                error_schema.append("Field 'validate_body_values' must be false")
            errors.append({"validate_schema": error_schema})
        if errors:
            raise ValidationError(errors, field_name="validate_*")


class RequestSchema(Schema):
    public_id = fields.UUID(dump_only=True)
    uri = fields.Str(required=True)
    method = EnumField(HTTPMethod, required=True,
                       error=f"Invalid value for method. Allowed values are {', '.join(HTTPMethod.__members__)}.")
    headers: dict = fields.Dict(required=False, missing={})
    query_params: list[str] = fields.List(fields.Str(), missing=[])
    body_schema: dict = fields.Dict(required=False, missing={})
    body: dict = fields.Dict(required=False, missing={})
    validate_schema: bool = fields.Boolean(missing=False)
    validate_query_params_key: bool = fields.Boolean(missing=False)
    validate_query_params_values: bool = fields.Boolean(missing=False)
    validate_header_key: bool = fields.Boolean(missing=False)
    validate_header_values: bool = fields.Boolean(missing=False)
    validate_body_key: bool = fields.Boolean(missing=False)
    validate_body_values: bool = fields.Boolean(missing=False)

    @post_load
    def make_instance(self, data, **kwargs):
        return Request(**data)
