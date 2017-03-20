""" Core Explore commons exceptions
"""


class UsernamePasswordRequiredError(Exception):
    """
        Exception raised when Username and Password are required
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
