"""
Geoserver Python API
"""
import json
import os
from pathlib import Path
from functools import wraps

import requests
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


@auth
def upload_shapefiles(workspace_name, store_name, file_path):
    """Upload a local .zip file which contains shapefiles.

    The "configure=all" will ensure that a new layer will be published for the uploaded file.

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefiles
    :param store_name: the name of datastore in which you would like to upload the shapefiles
    :param file_path: the local file path to your shapefiles(.zip)

    """
    # username, passwd, server_url = get_cfg()

    headers = {
        "Content-type": "application/zip",
        "Accept": "application/xml",
    }

    file_name = Path(file_path).stem
    url = (
        f"{server_url}/rest/workspaces/{workspace_name}/datastores"
        + f"/{store_name}/file.shp?filename={file_name}&update=overwrite&configure=all"
    )

    with open(file_path, "rb") as f:
        r = requests.put(
            url,
            data=f.read(),
            auth=(username, passwd),
            headers=headers,
        )
    return r


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
    # username, passwd, server_url = get_cfg()
    data_url = f"<url>file:{file_path}</url><filetype>shapefile</filetype>"
    data = f"<dataStore><name>{store_name}</name><connectionParameters>{data_url}</connectionParameters></dataStore>"
    headers = {"content-type": "text/xml"}

    url = f"{server_url}/rest/workspaces/{workspace_name}/datastores"
    r = requests.post(url, data, auth=(username, passwd), headers=headers)

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
    url = f"{server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}"
    r = requests.delete(url, auth=(username, passwd), params=payload)

    if r.status_code == 200:
        print(f"Datastore {store_name} has been deleted.")
    elif r.status_code == 404:
        print(f"Datastore {store_name} does not exist.")
    else:
        print(f"Error: {r.status_code} {r.content}")
    return r


@auth
def publish_layer(workspace_name, store_name, layer_name):
    """Publish a layer in the data store

    :param workspace_name: the name of the workspace in which the data store is
    :param store_name: the name of the data store in which the layer you would like to publish is
    :param layer_name: the name of layer which you would like to publish.
        the name could be the shapefiles name without .shp

    """
    # username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}/featuretypes/"

    layer_xml = f"<featureType><name>{layer_name}</name></featureType>"
    headers = {"content-type": "text/xml"}

    r = requests.post(
        url,
        data=layer_xml,
        auth=(username, passwd),
        headers=headers,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to publish layer {layer_name}. {r.status_code}, {r.content}")
    return r


@auth
def create_workspace(workspace_name):
    """create a workspace by name

    :param workspace_name: the name of the workspace which you would like to create

    """
    # username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/workspaces"
    data = f"<workspace><name>{workspace_name}</name></workspace>"
    headers = {"content-type": "text/xml"}
    r = requests.post(url, data=data, auth=(username, passwd), headers=headers)

    if r.status_code == 201:
        print(f"The workspace {workspace_name} has been created!")
    elif r.status_code in [401, 409]:
        print(f"The workspace {workspace_name} already exists.")
    else:
        print(f"Unable to create workspace {workspace_name}.")
    return r


@auth
def delete_workspace(workspace_name):
    """delete a workspace by name

    :param workspace_name: the name of the workspace which you would like to delete

    """
    # username, passwd, server_url = get_cfg()
    payload = {"recurse": "true"}
    url = f"{server_url}/rest/workspaces/{workspace_name}"
    r = requests.delete(url, auth=(username, passwd), params=payload)

    if r.status_code == 200:
        print(f"Workspace {workspace_name} has been deleted.")
    elif r.status_code == 404:
        print(f"Workspace {workspace_name} does not exist.")
    else:
        print(f"Error: {r.status_code} {r.content}")
    return r


@auth
def upload_raster(workspace_name, store_name, file_path, file_fmt):
    """Upload a local raster into geoserver.
        It seems that only one raster is allowed per coverage store unless using raster mosaic.

    :param workspace_name: the name of workspace
    :param store_name: the name of data store
    :param file_path: the local file path to the raster(.zip)
    :param file_fmt: such as geotiff

    """
    # username, passwd, server_url = get_cfg()

    headers = {"content-type": "application/zip", "Accept": "application/json"}

    # file_name = Path(file_path).stem
    url = (
        f"{server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/"
        + f"file.{file_fmt}?coverageName={store_name}&configure=all"
    )
    with open(file_path, "rb") as f:
        r = requests.put(url, data=f.read(), auth=(username, passwd), headers=headers)

        if r.status_code in [200, 201]:
            print(f"Coveragestores {store_name} was created/updated successfully")
        else:
            print(
                f"Unable to create Coveragestores {store_name}. Status code: {r.status_code}, { r.content}"
            )
        return r


@auth
def create_coveragestore(workspace_name, store_name, file_path):
    """Create a coverage store from a raster file on the geoserver.

    :param workspace_name: the name of workspace
    :param store_name: the name of the coverage store which you would like to create
    :param file_path: the file_path on the geoserver, relative to the "data_dir"
        You can find the "Data directory"/ "data_dir" in the "server status" page.

    """
    # username, passwd, server_url = get_cfg()
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

    url = f"{server_url}/rest/workspaces/{workspace_name}/coveragestores"
    r = requests.post(
        url, data=json.dumps(cfg), auth=(username, passwd), headers=headers
    )

    if r.status_code in [200, 201]:
        print(f"Datastore {store_name} was created/updated successfully")

    else:
        print(
            f"Unable to create datastore {store_name}. Status code: {r.status_code}, { r.content}"
        )
    return r


@auth
def publish_raster_layer(workspace_name, store_name, layer_name):
    """Publish a coverage/raster layer from a coverage store.
        It seems ,for some reason, that only one raster is allowed per coverage store.

    :param workspace_name: the name of the workspace
    :param store_name: the name of the coverage store in which the raster layer reside
    :param layer_name: the name of the raster layer

    """
    # username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/"

    layer_xml = f"<coverage><name>{layer_name}</name><nativeName>{layer_name}</nativeName></coverage>"
    headers = {"content-type": "text/xml"}

    r = requests.post(
        url,
        data=layer_xml,
        auth=(username, passwd),
        headers=headers,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to publish layer {layer_name}. {r.status_code}, {r.content}")
    return r


@auth
def add_style(style_name, workspace=None):
    """Add an empty style globally or into a workspace.

    :param style_name: the name of the style which you would like to create
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the new style will be a global one.

    """
    # username, passwd, server_url = get_cfg()
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{server_url}/rest/styles/"

    style_xml = (
        f"<style><name>{style_name}</name><filename>{style_name}.sld</filename></style>"
    )
    headers = {"content-type": "text/xml"}
    r = requests.post(url=url, data=style_xml, auth=(username, passwd), headers=headers)
    if r.status_code not in [200, 201]:
        print(f"Unable to create new style {style_name}. {r.content}")
    return r


@auth
def upload_style(style_name, file_path, workspace=None):
    """Upload a local sld file as a new style.
        The sytle must not exist yet.

    :param style_name: the name of the new style
    :param file_path: the local path to the .sld file
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the new style will be a global one.

    """
    # username, passwd, server_url = get_cfg()

    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{server_url}/rest/styles"

    header = {"content-type": "application/vnd.ogc.sld+xml"}
    # SLD 1.1 / SE 1.1 with a mime type of application/vnd.ogc.se+xml
    # SLD package(zip file containing sld and image files used in the style) with a mime type of application/zip

    payload = {"name": style_name, "raw": "true"}

    with open(file_path, "r") as f:
        style_data = f.read()
        r = requests.post(
            url,
            data=style_data,
            auth=(username, passwd),
            headers=header,
            params=payload,
        )
        if r.status_code not in [200, 201]:
            print(f"Unable to upload style {file_path}. {r.content}")
        return r


@auth
def modify_style(style_name, style_data, workspace=None):
    """Change an existing style.

    :param style_name: the name of the style
    :param style_data: the new data for the style
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the style is a global one.

    """
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{server_url}/rest/styles/{style_name}"

    header = {"content-type": "application/vnd.ogc.sld+xml"}

    r = requests.put(
        url,
        data=style_data,
        auth=(username, passwd),
        headers=header,
    )
    if r.status_code not in [200, 201]:
        print(f"Unable to modify style {style_name}. {r.content}")
    return r


@auth
def delete_style(style_name, workspace=None):
    """Delete a style by name

    :param style_name: the name of the style which you would like to delete
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the style is a global one.

    """
    # username, passwd, server_url = get_cfg()

    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{server_url}/rest/styles/{style_name}"

    r = requests.delete(
        url, auth=(username, passwd), params={"recurse": True, "purge": True}
    )

    if r.status_code in [200, 201]:
        print(f"Style {style_name} has been deleted. {r.status_code} {r.content}")
    else:
        print(f"Unable to delete {style_name}. {r.status_code} {r.content}")
    return r


@auth
def set_default_style(full_layer_name: str, full_style_name: str):
    """set the default style for a layer

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name
    :param full_style_name: str: the style name including the workspace_name,
        such as workspace_name:style_name

    """
    # username, passwd, server_url = get_cfg()

    headers = {"content-type": "application/json"}
    # headers = {"content-type": "text/xml"}
    url = f"{server_url}/rest/layers/{full_layer_name}"
    # style_xml = (
    #    f"<layer><defaultStyle><name>{full_style_name}</name></defaultStyle></layer>"
    # )
    # print(json_style)
    # json_style = {"defaultStyle": {"name": full_style_name}}
    json_style = {
        "layer": {"defaultStyle": {"name": full_style_name}},
    }

    r = requests.put(
        url,
        data=json.dumps(json_style),
        # data=style_xml,
        auth=(username, passwd),
        headers=headers,
    )

    if r.status_code in [200, 201]:
        print(
            f"The default style for layer {full_layer_name } has been set to {full_style_name}. {r.status_code} {r.content}"
        )
    else:
        print(
            f"Unable to set default style {full_style_name} for layer {full_layer_name}. {r.status_code} {r.text}"
        )


@auth
def add_additional_style(full_layer_name: str, full_style_name: str):
    """Add an additional style to a layer.

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name
    :param full_style_name: str: the style name including the workspace_name,
        such as workspace_name:style_name

    """
    # username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/layers/{full_layer_name}"

    headers = {"content-type": "text/xml"}
    r = requests.put(
        url,
        data=f"<layer><styles><style><name>{full_style_name}</name></style></styles></layer>",
        auth=(username, passwd),
        headers=headers,
    )

    if r.status_code in [200, 201]:
        print(
            f"The additional style {full_style_name} for layer {full_layer_name } has been added. {r.status_code} {r.content}"
        )
    else:
        print(
            f"Unable to add additional style {full_style_name} for layer {full_layer_name}. {r.status_code} {r.content}"
        )


@auth
def get_layer_styles(full_layer_name: str):
    """Get the styles associated with a layer

    :param full_layer_name: str: the layer name including the workspace_name,
        such as workspace_name:layer_name

    """
    # username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/layers/{full_layer_name}/styles"

    r = requests.get(
        url,
        auth=(username, passwd),
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
def get_layer(layer_name: str, workspace=None):
    """Get the definition of the layer

    :param layer_name: str: the name of the layer to retrieve
    :param workspace:  (Default value = None) if the workspace name is not given,
        return the first layer which matches the given layer name. This is odd!

    """
    # username, passwd, server_url = get_cfg()
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/layers/{layer_name}"
    else:
        url = f"{server_url}/rest/layers/{layer_name}"
    r = requests.get(
        url,
        auth=(username, passwd),
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
    # username, passwd, server_url = get_cfg()
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/layers"
    else:
        url = f"{server_url}/rest/layers"
    r = requests.get(
        url,
        auth=(username, passwd),
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
    """Delete a layer by name

    :param layer_name: the name of the layer which you would like to delete
    :param workspace:  (Default value = None) If the workspace name is not given,
        delete the first layer which matches the given layer name. This is odd!

    """
    # username, passwd, server_url = get_cfg()
    payload = {"recurse": "true"}

    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/layers/{layer_name}"
    else:
        url = f"{server_url}/rest/layers/{layer_name}"

    r = requests.delete(
        url=url,
        params=payload,
        auth=(username, passwd),
    )
    if r.status_code in [200, 201]:
        print(f"layer:{layer_name} has been deleted!")
        return True
    else:
        print(f"Failed to delete layer:{layer_name}")
        print(r.text)
        return False


@auth
def get_styles(workspace=None):
    """Get all global styles or all styles in a workspace

    :param workspace:  (Default value = None) If the workspace name is not given,
        all global styles will be returned.

    """
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{server_url}/rest/styles"
    r = requests.get(
        url,
        auth=(username, passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "style" in data["styles"]:
            ret = [d["name"] for d in data["styles"]["style"]]
        return ret
    else:
        return None


@auth
def get_all_workspaces():
    """Get the names of all workspaces"""
    url = f"{server_url}/rest/workspaces"
    r = requests.get(
        url,
        auth=(username, passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        ret = []
        data = r.json()
        if "workspace" in data["workspaces"]:
            ret = [d["name"] for d in data["workspaces"]["workspace"]]
        return ret
    else:
        return None


@auth
def get_workspace(name):
    """Get the definition of a workspace

    :param name: the name of the workspace in which you are interested

    """
    url = f"{server_url}/rest/workspaces/{name}"
    r = requests.get(
        url,
        auth=(username, passwd),
    )
    # print(r.json())
    if r.status_code in [200, 201]:
        return r.json()
    else:
        return None


@auth
def get_datastores(workspace):
    """Get datastores in a workspace

    :param workspace: the name of the workspace in which you are interested

    """
    url = f"{server_url}/rest/workspaces/{workspace}/datastores"
    r = requests.get(
        url,
        auth=(username, passwd),
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
