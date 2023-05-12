import json

import requests

from . import _auth as a
from ._auth import auth


@auth
def create_store(workspace_name, store_name, file_path):
    """Create a datastore from a folder or .shp on the server.
        The folder or .shp must have already been on the server.

    :param workspace_name: the name of destine workspace in which you would like to
        create the data store
    :param store_name: the name of data store which you would like to create
    :param file_path: the file_path on the geoserver, relative to the "data_dir"
        (can be a path or a .shp file).
        You can find the "Data directory"/ "data_dir" in the "server status" page.

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    data_url = f"<url>file:{file_path}</url><filetype>shapefile</filetype>"
    data = f"<dataStore><name>{store_name}</name><connectionParameters>{data_url}</connectionParameters></dataStore>"
    headers = {"content-type": "text/xml"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"
    r = requests.post(url, data, auth=(a.username, a.passwd), headers=headers)

    if r.status_code in [200, 201]:
        print(f"Datastore {store_name} was created/updated successfully")

    else:
        print(
            f"Unable to create datastore {store_name}. Status code: {r.status_code}, { r.content}"
        )
    return r


@auth
def delete_store(workspace_name, store_name):
    """Delete a data store by name.

    :param workspace_name: the name of workspace in which the data store is
    :param store_name: the name of data store which you would like to delete

    """
    payload = {"recurse": "true"}
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}"
    r = requests.delete(url, auth=(a.username, a.passwd), params=payload)

    if r.status_code == 200:
        print(f"Datastore {store_name} has been deleted.")
    elif r.status_code == 404:
        print(f"Datastore {store_name} does not exist.")
    else:
        print(f"Error: {r.status_code} {r.content}")
    return r


@auth
def get_datastores(workspace):
    """Get datastores in a workspace

    :param workspace: the name of the workspace in which you are interested

    """
    url = f"{a.server_url}/rest/workspaces/{workspace}/datastores"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "dataStore" in data["dataStores"]:
            ret = [d["name"] for d in data["dataStores"]["dataStore"]]
        return ret
    else:
        return None


@auth
def create_coveragestore(workspace_name, store_name, file_path):
    """Create a coverage store from a raster file on the geoserver.

    :param workspace_name: the name of workspace
    :param store_name: the name of the coverage store which you would like to create
    :param file_path: the file_path on the geoserver, relative to the "data_dir"
        You can find the "Data directory"/ "data_dir" in the "server status" page.

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    cfg = {
        "coverageStore": {
            "name": store_name,
            "type": "GeoTIFF",
            "enabled": True,
            "_default": False,
            "workspace": {"name": workspace_name},
            "url": f"file:{file_path}",
        }
    }

    headers = {"content-type": "application/json"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores"
    r = requests.post(
        url, data=json.dumps(cfg), auth=(a.username, a.passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(f"Datastore {store_name} was created/updated successfully")

    else:
        print(
            f"Unable to create datastore {store_name}. Status code: {r.status_code}, { r.content}"
        )
    return r
