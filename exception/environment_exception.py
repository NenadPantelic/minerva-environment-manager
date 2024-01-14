class EnvironmentException(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self._message = message
        self._status = status

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message
