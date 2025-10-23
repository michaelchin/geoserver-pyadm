import json

import requests

from . import _auth as a
from ._auth import auth


@auth
def reindex_image_mosaic_store(workspace_name, store_name, path):
    """Reindex an image mosaic store. Re-populate the store with the files in the given path.

    :param workspace_name: workspace name
    :param store_name: image mosaic store name
    :param path: the path which contains the raster files

    """

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/external.imagemosaic"
    headers = {"Content-type": "text/plain"}

    r = requests.post(url, auth=(a.username, a.passwd), data=path, headers=headers)

    if r.status_code in [200, 201, 202]:
        print(f"Store {store_name} has been reindexed.")
    else:
        print(r.text)
        print(r.status_code)
    return r


@auth
def add_raster_to_image_mosaic_store(workspace_name, store_name, filepath):
    """Add a new raster file into the image mosaic store. The raster file must be in the server.
        Geoserver calls this process "harvesting".

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
def get_rasters_in_coverage(
    workspace_name, store_name, coverage_name, return_details=False
):
    """Return all the granules in a coverage within an image mosaic store.

    :param workspace_name: workspace name
    :param store_name: image mosaic store name
    :param coverage_name: the coverage name
    :param return_details: if True, return all details about the granules
        if False, only return id and location.

    """

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}/index/granules.json"

    r = requests.get(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        data = r.json()
        if return_details:
            ret = data
        else:
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
        print(url)
        return []


@auth
def delete_raster_from_coverage(workspace_name, store_name, coverage_name, id):
    """Delete a raster from a coverage within an image mosaic store

    :param workspace_name: workspace name
    :param store_name: image mosaic store name
    :param coverage_name: the coverage name
    :param id: the raster id which can be retrieved by calling get_rasters_in_coverage()

    """
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/{coverage_name}/index/granules/{id}.xml"
    print(url)
    r = requests.delete(url, auth=(a.username, a.passwd))

    if r.status_code in [200, 201]:
        print(f"Deleted raster {id} from coverage {coverage_name}")
    else:
        print(r.text)
        print(r.status_code)
    return r


@auth
def enable_time_dimension(workspace_name, store_name, coverage_name):
    """Enable time dimension for a coverage within a image mosaic store.

    :param workspace_name: workspace name
    :param store_name: coverage store name
    :param coverage_name: the name of the new coverage

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
