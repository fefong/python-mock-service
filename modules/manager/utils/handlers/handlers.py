from marshmallow import ValidationError

from modules.manager.utils.builders.responses_builder import ResponseBuilder


class Handlers:

    MESSAGE_VALIDATION_FAIL = "Validation failure"

    @staticmethod
    def handler_validation_error(validation_error: ValidationError):
        errors = []
        for field, message in validation_error.messages.items():
            errors.append({
                "field": field,
                "message": message
            })
        return ResponseBuilder.response_fail(message=Handlers.MESSAGE_VALIDATION_FAIL,
                                             errors=errors)
