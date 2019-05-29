""" Common tools for protocols
"""
from builtins import str


def get_url(protocol, address, port):
    """ Returns the Url with the given parameters

    Args:
        protocol:
        address:
        port:

    Returns:

    """
    return protocol + "://" + address + ":" + str(port)
