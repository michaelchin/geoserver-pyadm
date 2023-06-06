import json
import os

import requests

from . import _auth as a
from ._auth import auth
from ._exceptions import (
    FailedToCreateDatastore,
    DatastoreAlreadyExists,
    FailedToDeleteDatastore,
    DatastoreDoesNotExists,
)


@auth
def create_datastore(workspace_name, store_name, file_path, is_dir=False):
    """Create a datastore from a folder or .shp on the server.
        The folder or .shp must have already been on the server.

    :param workspace_name: the name of destine workspace in which you would like to
        create the data store
    :param store_name: the name of data store which you would like to create
    :param file_path: the file_path on the geoserver, relative to the "data_dir"
        (can be a path or a .shp file).
        You can find the "Data directory"/ "data_dir" in the "server status" page.
    :param is_dir: flag to indicate if the store is a shapefile directory

    """
    if is_dir:
        store_type = "Directory of spatial files (shapefiles)"
    else:
        store_type = "shapefile"

    cfg = {
        "dataStore": {
            "name": store_name,
            "type": store_type,
            "connectionParameters": {
                "entry": [
                    {"@key": "filetype", "$": "shapefile"},
                    {"@key": "url", "$": f"file:{file_path}"},
                    {"@key": "fstype", "$": "shape"},
                ]
            },
        }
    }

    headers = {"content-type": "application/json"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"

    r = requests.post(
        url, data=json.dumps(cfg), auth=(a.username, a.passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(f"Datastore {store_name} has been created successfully.")
    elif "already exists" in r.text:
        raise DatastoreAlreadyExists(store_name)
    else:
        raise FailedToCreateDatastore(store_name)
    return r


@auth
def delete_datastore(workspace_name, store_name):
    """Delete a data store by name.

    :param workspace_name: the name of workspace in which the data store is
    :param store_name: the name of data store which you would like to delete

    """
    payload = {"recurse": "true"}
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}"

    r = requests.delete(url, auth=(a.username, a.passwd), params=payload)

    if r.status_code == 200:
        print(f"Datastore {workspace_name}:{store_name} has been deleted.")
    elif r.status_code == 404:
        raise DatastoreDoesNotExists(f"{workspace_name}:{store_name}")
    else:
        raise FailedToDeleteDatastore(f"{workspace_name}:{store_name}")
    return r


@auth
def get_datastores(workspace):
    """Get all datastores in a workspace

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
def create_geopackage_store(workspace_name, store_name, file_path):
    """Create a datastore from a geopackage file.
        The geopackage file must have already been on the server.

    :param workspace_name: the name of destine workspace in which you would like to
        create the data store
    :param store_name: the name of data store which you would like to create
    :param file_path: the file_path on the geoserver, relative to the "data_dir"
        (can be a path or a .shp file).
        You can find the "Data directory"/ "data_dir" in the "server status" page.

    """
    cfg = {
        "dataStore": {
            "name": store_name,
            "type": "GeoPackage",
            "connectionParameters": {
                "entry": [
                    {
                        "@key": "database",
                        "$": f"file:{file_path}",
                    },
                    {"@key": "dbtype", "$": "geopkg"},
                ]
            },
        }
    }

    headers = {"content-type": "application/json"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"

    r = requests.post(
        url, data=json.dumps(cfg), auth=(a.username, a.passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(f"Datastore {store_name} has been created successfully.")
    elif "already exists" in r.text:
        raise DatastoreAlreadyExists(store_name)
    else:
        raise FailedToCreateDatastore(store_name)
    return r
