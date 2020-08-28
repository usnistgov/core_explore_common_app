""" Core Explore Common exceptions
"""


class UsernamePasswordRequiredError(Exception):
    """
    Exception raised when Username and Password are required
    """

    def __init__(self, message):
        self.message = message


class ExploreRequestError(Exception):
    """
    Exception raised when an error occurs in the request
    """

    def __init__(self, message):
        self.message = message
