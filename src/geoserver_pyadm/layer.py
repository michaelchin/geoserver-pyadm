import requests, json

from . import _auth as a
from ._auth import auth

from . import coveragestore


@auth
def publish_layer(workspace_name, store_name, layer_name):
    """Publish a layer in the data store

    :param workspace_name: the name of the workspace in which the data store is
    :param store_name: the name of the data store in which the layer you would like to publish is
    :param layer_name: the name of layer which you would like to publish.
        the name could be the shapefiles name without .shp

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}/featuretypes/"

    layer_xml = f"<featureType><name>{layer_name}</name></featureType>"
    headers = {"content-type": "text/xml"}

    r = requests.post(
        url,
        data=layer_xml,
        auth=(a.username, a.passwd),
        headers=headers,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to publish layer {layer_name}. {r.status_code}, {r.content}")
    return r


@auth
def publish_raster_layer(workspace_name, store_name, layer_name, native_name=None):
    """Publish a coverage/raster layer from a coverage store.
        It seems ,for some reason, that only one raster is allowed per coverage store.

    :param workspace_name: the name of the workspace
    :param store_name: the name of the coverage store in which the raster layer reside
    :param layer_name: the name of the raster layer
    :param native_name: the native name must be the same with the file name. if None, try to get the file name from store

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/"

    if not native_name:
        r = coveragestore.get_coverage_store_info(workspace_name, store_name)
        filename = r["coverageStore"]["url"].split("/")[-1]
        ext = filename.split(".")[-1]
        native_name = filename[: -len(ext) - 1]

    layer_xml = f"<coverage><name>{layer_name}</name><nativeName>{native_name}</nativeName></coverage>"
    headers = {"content-type": "text/xml"}

    r = requests.post(
        url,
        data=layer_xml,
        auth=(a.username, a.passwd),
        headers=headers,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to publish layer {layer_name}. {r.status_code}, {r.content}")
    return r


@auth
def get_layer(layer_name: str, workspace=None):
    """Get the definition of the layer

    :param layer_name: str: the name of the layer to retrieve
    :param workspace:  (Default value = None) if the workspace name is not given,
        return the first layer which matches the given layer name. This is odd!

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/layers/{layer_name}"
    else:
        url = f"{a.server_url}/rest/layers/{layer_name}"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        return r.json()
    else:
        return None


@auth
def get_layers(workspace=None):
    """Get all the layers in geoserver if workspace name is not given.
        Return all the layers in a workspace if workspace name is given.

    :param workspace:  (Default value = None) If workspace name is not given,
        the function will return all the layers in the geoserver.

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/layers"
    else:
        url = f"{a.server_url}/rest/layers"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "layer" in data["layers"]:
            ret = [d["name"] for d in data["layers"]["layer"]]
        return ret

    return None


@auth
def delete_layer(layer_name, workspace=None):
    """Delete a layer/layers by name

    :param layer_name: the name of the layer which you would like to delete
    :param workspace:  (Default value = None) If the workspace name is not given,
        delete all layers with the given name.

    """
    payload = {"recurse": "True", "quietOnNotFound": "True"}

    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/layers/{layer_name}"
        r = requests.delete(
            url=url,
            params=payload,
            auth=(a.username, a.passwd),
        )
        if r.status_code in [200, 201]:
            print(f"The layer {layer_name} has been deleted!")
            return r.content
        else:
            print(f"Failed to delete layer:{layer_name}")
            return r.content
    else:
        url = f"{a.server_url}/rest/layers/{layer_name}"
        while True:
            r = requests.delete(
                url=url,
                params=payload,
                auth=(a.username, a.passwd),
            )
            if r.status_code not in [200, 201]:
                break
            else:
                print(f"The layer {layer_name} has been deleted!")
            # print(r.content)
        return "done"


@auth
def get_layer_styles(full_layer_name: str):
    """Get the styles associated with a layer

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/layers/{full_layer_name}/styles"

    r = requests.get(
        url,
        auth=(a.username, a.passwd),
    )
    # print(r.content)
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "style" in data["styles"]:
            ret = [d["name"] for d in data["styles"]["style"]]
        return ret
    else:
        return None


@auth
def publish_geopackage_layer(
    workspace_name, store_name, layer_name, geom_type="polygon"
):
    """Publish a geopackage layer in the data store

    :param workspace_name: the name of the workspace in which the data store is
    :param store_name: the name of the data store in which the layer you would like to publish is
    :param layer_name: the name of geopackage layer which you would like to publish.

    """
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}/featuretypes/"

    layer_cfg = {
        "featureType": {
            "name": f"{layer_name}_{geom_type}",
            "nativeName": f"{layer_name}_{geom_type}",
            "title": f"{layer_name}_{geom_type}",
        }
    }
    headers = {"content-type": "application/json"}

    r = requests.post(
        url,
        data=json.dumps(layer_cfg),
        auth=(a.username, a.passwd),
        headers=headers,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to publish layer {layer_name}. {r.status_code}, {r.content}")
    return r
