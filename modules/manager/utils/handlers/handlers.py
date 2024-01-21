from marshmallow import ValidationError

from modules.manager.utils.builders.responses_builder import ResponseBuilder


class Handlers:

    MESSAGE_VALIDATION_FAIL = "Validation failure"

    @staticmethod
    def handler_validation_error(ex: ValidationError):
        errors = []
        for field, message in ex.messages.items():
            errors.append({"field": field, "message": message})
        return ResponseBuilder.response_fail(Handlers.MESSAGE_VALIDATION_FAIL, errors)
