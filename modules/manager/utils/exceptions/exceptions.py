
MESSAGE_NOT_FOUND = '{} not found'


class NotFoundError(Exception):
    def __init__(self, name, message: str = None, metadata: dict = None):
        self.name = name
        self.message = message or MESSAGE_NOT_FOUND.format(name)
        self.metadata = metadata or None
        super().__init__(self.message)
