class NotSupportedError(Exception):
    """Exception raised for operations that are not supported."""

    def __init__(self, message="This operations is not supported."):
        self.message = message
        super().__init__(self.message)
