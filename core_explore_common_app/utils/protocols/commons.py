""" Common tools for protocols
"""


def get_url(protocol, address, port):
    """Returns the Url with the given parameters

    Args:
        protocol:
        address:
        port:

    Returns:

    """
    return protocol + "://" + address + ":" + str(port)
