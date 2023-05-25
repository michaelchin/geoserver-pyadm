import json
import os

import requests

from . import _auth as a
from ._auth import auth


@auth
def get_coverage_stores(workspace_name):
    """return a list of names of coverage store within a workspace

    :param workspace_name: workspace name

    """
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores.json"

    r = requests.get(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "coverageStore" in data["coverageStores"]:
            ret = [d["name"] for d in data["coverageStores"]["coverageStore"]]
        return ret
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def get_coverage_store_info(workspace_name, store_name):
    """return the coverage store configuration in json format

    :param workspace_name: workspace name
    :param store_name: coverage store name

    """
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}.json"

    r = requests.get(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def reindex_existing_image_mosaic_store(workspace_name, store_name, path):
    """ """

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/external.imagemosaic"
    headers = {"Content-type": "text/plain"}

    r = requests.post(url, auth=(a.username, a.passwd), data=path, headers=headers)

    if r.status_code in [200, 201]:
        return r.json()
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def add_raster_to_image_mosaic_store(workspace_name, store_name, filepath):
    """Add a new raster file into the image mosaic store. The raster file must be in the server.

    :param workspace_name: workspace name
    :param store_name: image mosaic store name
    :param filepath: the location of the new raster file in the server

    """

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/external.imagemosaic"
    headers = {"Content-type": "text/plain"}

    r = requests.post(url, auth=(a.username, a.passwd), data=filepath, headers=headers)

    if r.status_code in [200, 201, 202]:
        print(f"The new raster has been added to store {store_name}.")
    else:
        print(f"Failed to add the new raster to store {store_name}.")
    return r


@auth
def get_rasters_in_image_mosaic_store(workspace_name, store_name, coverage_name):
    """"""

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}/index/granules.json"
    print(url)
    r = requests.get(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        data = r.json()
        ret = [
            {
                "id": d["id"],
                # "time": d["properties"]["time"],
                # "elevation": d["properties"]["elevation"],
                "location": d["properties"]["location"],
            }
            for d in data["features"]
        ]
        return ret
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def delete_raster_from_image_mosaic_store(
    workspace_name, store_name, coverage_name, id
):
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}/index/granules/{id}.xml"
    print(url)
    r = requests.delete(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        return id
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def delete_coverage_store(workspace_name, store_name):
    url = (
        f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/"
    )
    print(url)
    payload = {"recurse": "true", "purge": "none"}
    r = requests.delete(url, auth=(a.username, a.passwd), params=payload)

    if r.status_code in [200, 201]:
        return id
    else:
        print(r.text)
        print(r.status_code)
        return None


@auth
def create_coverage_store(workspace_name, store_name, file_path):
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


@auth
def create_coverage(workspace_name, store_name, coverage_name):
    """Create a coverage within a coverage store. It is more like publishing a layer?
    Anyway, it is useful for image mosaic stores, which allows multiple coverages in one store.

    param workspace_name: workspace name
    param store_name: coverage store name
    param coverage_name: the name of the new coverage

    """
    cfg = {
        "coverage": {
            "name": coverage_name,
            "nativeName": coverage_name,
            "nativeCoverageName": coverage_name,
        }
    }

    headers = {"content-type": "application/json"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages"
    r = requests.post(
        url, data=json.dumps(cfg), auth=(a.username, a.passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(f"Coverage {coverage_name} was created/updated successfully")

    else:
        print(
            f"Unable to create coverage {coverage_name}. Status code: {r.status_code}, { r.content}"
        )
    return r


@auth
def enable_time_dimension(workspace_name, store_name, coverage_name):
    """Enable time dimension for a coverage within a image mosaic store.

    param workspace_name: workspace name
    param store_name: coverage store name
    param coverage_name: the name of the new coverage

    """
    cfg = {
        "coverage": {
            "name": coverage_name,
            "nativeName": coverage_name + "N",
            "enabled": True,
            "metadata": {
                "entry": [
                    {
                        "@key": "time",
                        "dimensionInfo": {
                            "enabled": True,
                            "presentation": "LIST",
                            "units": "ISO8601",
                        },
                    },
                ]
            },
        }
    }

    headers = {"content-type": "application/json"}

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}"
    r = requests.put(
        url, data=json.dumps(cfg), auth=(a.username, a.passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(
            f"Time dimension has been created/updated successfully for {coverage_name}."
        )

    else:
        print(f"Unable to enable time dimension for {coverage_name}. ")
    return r
