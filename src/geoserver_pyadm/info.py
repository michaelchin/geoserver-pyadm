import requests

from . import _auth as a
from ._auth import auth


@auth
def get_global_settings():
    """Get GeoServer’s global settings."""
    url = f"{a.server_url}/rest/settings"
    headers = {"Accept": "application/json"}

    r = requests.get(
        url,
        auth=(a.username, a.passwd),
        headers=headers,
    )
    return r.json()


@auth
def get_status():
    """Get GeoServer’s status."""
    url = f"{a.server_url}/rest/about/status"
    headers = {"Accept": "application/json"}

    r = requests.get(
        url,
        auth=(a.username, a.passwd),
        headers=headers,
    )
    return r.json()


@auth
def get_version():
    """Get GeoServer’s version."""
    url = f"{a.server_url}/rest//about/version"
    headers = {"Accept": "application/json"}

    r = requests.get(
        url,
        auth=(a.username, a.passwd),
        headers=headers,
    )
    return r.json()
