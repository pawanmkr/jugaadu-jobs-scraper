class DatabaseWriteError(Exception):
    """Raised when a write operation to the database fails.

    Attributes:
        message (str): Explanation of the error.
        original_exception: The original exception that triggered this error.

    """

    def __init__(self, message: str, original_exception: Exception) -> None:
        """Initialize the DatabaseWriteError.

        Args:
            message (str): Description of the error.
            original_exception: The original exception that caused this error.

        """
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self) -> str:
        """Return a string representation of the exception.

        Includes the original exception if present.
        """
        if self.original_exception:
            return f"{self.message} (caused by {self.original_exception!r})"
        return self.message
