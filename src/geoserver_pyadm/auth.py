import os
from functools import wraps

from dotenv import load_dotenv

script_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

username = None
passwd = None
server_url = None


def auth(func):
    """decorator to get server authentication info

    :param func: the user's function which this decorator will wrap around.

    """

    @wraps(func)
    def inner(*args, **kwargs):
        """the wrapper function

        :param *args: allow the inner function to accept multiple positional arguments
        :param **kwargs: allow the inner function to accept multiple keyword (or named) arguments.

        """
        global username
        global passwd
        global server_url
        if not username or not passwd or not server_url:
            username, passwd, server_url = get_cfg()
        return func(*args, **kwargs)

    return inner


def get_env():
    """Get username, password and url from environment."""
    return (
        os.environ.get("GEOSERVER_USERNAME"),
        os.environ.get("GEOSERVER_PASSWORD"),
        os.environ.get("GEOSERVER_URL"),
    )


def get_cfg():
    """Get the server configuration, such as username, password, geoserver URL
    either from environment variables or .env file.

    """
    # first, try to get the info from environment variables
    username, passwd, server_url = get_env()
    # if cound not get all info from environment variables
    # try to load .env file
    if not all([username, passwd, server_url]):
        # load environment variables from .env.
        load_dotenv(f"{cwd}/.env")
        username, passwd, server_url = get_env()
        # still failed? inform caller something is wrong
        if not all([username, passwd, server_url]):
            raise (
                "set env variables GEOSERVER_USERNAME, GEOSERVER_PASSWORD, GEOSERVER_URL and then retry"
            )
    return username, passwd, server_url
