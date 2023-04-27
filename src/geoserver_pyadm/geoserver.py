import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

script_path = os.path.dirname(os.path.realpath(__file__))

#
# get username password url from environment
#
def get_env():
    return (
        os.environ.get("GEOSERVER_USERNAME"),
        os.environ.get("GEOSERVER_PASSWORD"),
        os.environ.get("GEOSERVER_URL"),
    )


#
#
#
def get_cfg():
    username, passwd, server_url = get_env()
    if not all([username, passwd, server_url]):
        load_dotenv(f"{script_path}/.env")  # take environment variables from .env.
        username, passwd, server_url = get_env()
        if not all([username, passwd, server_url]):
            raise (
                "set env variables GEOSERVER_USERNAME, GEOSERVER_PASSWORD, GEOSERVER_URL"
            )
    return username, passwd, server_url


#
# upload a local .zip file which contains shapefiles
# the "configure=all" will ensure that a new layer will be published for the uploaded file.
#
def upload_shapefiles(workspace_name, store_name, file_path):
    username, passwd, server_url = get_cfg()

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


#
# The file_path can be a path or a .shp file
# The file_path can be relative to the "data_dir".
# You can find the "Data directory"/ "data_dir" in the "server status" page.
def create_store(workspace_name, store_name, file_path):
    username, passwd, server_url = get_cfg()
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


#
# publish the shapefiles in the store folder
# the layer_name is the shapefiles name without .shp
def publish_layer(workspace_name, store_name, layer_name):
    username, passwd, server_url = get_cfg()
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


#
#
def create_workspace(workspace_name):
    username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/workspaces"
    data = f"<workspace><name>{workspace_name}</name></workspace>"
    headers = {"content-type": "text/xml"}
    r = requests.post(url, data=data, auth=(username, passwd), headers=headers)

    if r.status_code == 201:
        print(f"The workspace {workspace_name} has been created!")
    elif r.status_code == 401:
        print(f"The workspace {workspace_name} already exists.")

    else:
        print(f"Unable to create workspace {workspace_name}.")


#
#
def delete_workspace(workspace_name):
    username, passwd, server_url = get_cfg()
    payload = {"recurse": "true"}
    url = f"{server_url}/rest/workspaces/{workspace_name}"
    r = requests.delete(url, auth=(username, passwd), params=payload)

    if r.status_code == 200:
        print(f"Workspace {workspace_name} has been deleted.")
    elif r.status_code == 404:
        print(f"Workspace {workspace_name} does not exist.")
    else:
        print(f"Error: {r.status_code} {r.content}")


#
# it seems that only one raster is allowed per coverage store unless using raster mosaic
#
def upload_raster(workspace_name, store_name, file_path, file_fmt):
    username, passwd, server_url = get_cfg()

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


#
#
def create_coveragestore(workspace_name, store_name, file_path):
    username, passwd, server_url = get_cfg()
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


#
# publish a coverage/raster layer from a coverage store
# it seems that only one raster is allowed per coverage store
#
def publish_raster_layer(workspace_name, store_name, layer_name):
    username, passwd, server_url = get_cfg()
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


#
#
def add_style(style_name, workspace=None):
    username, passwd, server_url = get_cfg()
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


#
#
def upload_style(style_name, file_path, workspace=None):
    username, passwd, server_url = get_cfg()

    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{server_url}/rest/styles/{style_name}"

    header = {"content-type": "application/vnd.ogc.sld+xml"}

    with open(file_path, "rb") as f:
        r = requests.put(
            url,
            data=f.read(),
            auth=(username, passwd),
            headers=header,
        )
        if r.status_code not in [200, 201]:
            print(f"Unable to upload style {file_path}. {r.content}")


#
#
def delete_style(style_name, workspace=None):
    username, passwd, server_url = get_cfg()

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


#
# set the default style for a layer
# the "full_layer_name" includes the workspace_name, such as  workspace_name:layer_name
# the "full_style_name" includes the workspace_name, such as  workspace_name:style_name
#
def set_default_style(full_layer_name: str, full_style_name: str):
    username, passwd, server_url = get_cfg()

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


#
# add additional style to a layer
# the "full_layer_name" includes the workspace_name, such as  workspace_name:layer_name
# the "full_style_name" includes the workspace_name, such as  workspace_name:style_name
#
def add_additional_style(full_layer_name: str, full_style_name: str):
    username, passwd, server_url = get_cfg()
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


#
#
# the "full_layer_name" includes the workspace_name, such as  workspace_name:layer_name
#
def get_styles(full_layer_name: str):
    username, passwd, server_url = get_cfg()
    url = f"{server_url}/rest/layers/{full_layer_name}/styles"

    r = requests.get(
        url,
        auth=(username, passwd),
    )
    print(r.content)
    if r.status_code in [200, 201]:
        return json.loads(r.content)
    else:
        return None


#
#
def get_layer(layer_name: str, workspace=None):
    username, passwd, server_url = get_cfg()
    if workspace:
        url = f"{server_url}/rest/workspaces/{workspace}/layers/{layer_name}"
    else:
        url = f"{server_url}/rest/layers/{layer_name}"
    r = requests.get(
        url,
        auth=(username, passwd),
    )
    print(r.json())
    if r.status_code in [200, 201]:
        return r.json()
    else:
        return None


#
# Get all the layers from geoserver
# If workspace is None, it will list all the layers from geoserver
#
def get_layers(workspace=None):
    username, passwd, server_url = get_cfg()
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
        layers = r.json()["layers"]
        if "layer" in layers:
            return layers["layer"]

    return None


#
#
#
def delete_layer(layer_name, workspace=None):
    username, passwd, server_url = get_cfg()
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
