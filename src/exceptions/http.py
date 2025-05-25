"""A handy Exception class."""


class NotOkError(Exception):
    """Handles error which are not OK (200)."""

    def __init__(self, status_code: int, message: str) -> None:
        """Initialize a NotOkError with status code and message.

        Args:
            status_code (int): HTTP status code
            message (str): Error message or reason

        """
        super().__init__("Error, Got: %d with Reason - %d", status_code, message)
