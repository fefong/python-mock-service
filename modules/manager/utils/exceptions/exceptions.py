from modules.manager.utils.enums.names_enum import NamesEnum

MESSAGE_NOT_FOUND = '{} not found'
MESSAGE_CONFLICT = '{} already registered'


class NotFoundError(Exception):
    def __init__(self, name: NamesEnum, message: str = None, metadata: dict = None):
        self.name = name
        self.message = message or MESSAGE_NOT_FOUND.format(name.value)
        self.metadata = metadata or None
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, name: NamesEnum, message: str = None, metadata: dict = None):
        self.name = name
        self.message = message or MESSAGE_CONFLICT.format(name.value)
        self.metadata = metadata or None
        super().__init__(self.message)
