"""
Geoserver Python API
"""
import glob
import json
import os
import tempfile
import zipfile
from pathlib import Path

import requests

from auth import auth
from workspace import create_workspace, delete_workspace

import auth as a


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


@auth
def upload_shapefile_zip(workspace_name, store_name, file_path, configure="none"):
    """Upload a local .zip file which contains shapefile.
        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefile
    :param store_name: the name of datastore in which you would like to upload the shapefile
    :param file_path: the local file path to your shapefile(.zip)
    :param configure: this parameter takes three possible values
        "first" —- (Default) Only setup the first feature type available in the data store.
        "none"  —- Do not configure any feature types.
        "all"   —- Configure all feature types.

    """
    # a.username, a.passwd, a.server_url = get_cfg()

    headers = {
        "Content-type": "application/zip",
        "Accept": "application/xml",
    }

    file_name = Path(file_path).stem
    url = (
        f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"
        + f"/{store_name}/file.shp?filename={file_name}&update=overwrite&configure={configure}"
    )

    with open(file_path, "rb") as f:
        r = requests.put(
            url,
            data=f.read(),
            auth=(a.username, a.passwd),
            headers=headers,
        )
    return r


def upload_shapefile(workspace_name, store_name, file_path, configure="none"):
    """Upload a local shapefile. A shapefile may contain several files.
        You need to specify the path of the .shp file.

        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefile
    :param store_name: the name of datastore in which you would like to upload the shapefile
    :param file_path: the local path to your shapefile, such as xxxxxx.shp
    :param configure: this parameter takes three possible values
        first—(Default) Only setup the first feature type available in the data store.
        none—Do not configure any feature types.
        all—Configure all feature types.

    """
    p = Path(file_path)
    file_name = p.stem
    ext = p.suffix

    if ext == ".zip":
        return upload_shapefile_zip(workspace_name, store_name, file_path, configure)
    elif ext == ".shp":
        with tempfile.TemporaryDirectory() as tmp_dir:
            files = glob.glob(f"{file_path[:-4]}.*")
            with zipfile.ZipFile(f"{tmp_dir}/{file_name}.zip", "w") as tmp_zip:
                for f in files:
                    tmp_zip.write(f, os.path.basename(f))
            t = f"{tmp_dir}/{file_name}.zip"
            return upload_shapefile_zip(
                workspace_name, store_name, f"{tmp_dir}/{file_name}.zip", configure
            )
    else:
        raise Exception(f"Unsupported file extension: {file_path}")


def upload_shapefile_folder(workspace_name, store_name, folder_path, configure="none"):
    """Upload all the shapefiles within a local folder. The shapefiles can be .zip files or separate files.
        Make sure your .zip is valid. If there is a folder in your .zip file, the upload will fail.
        For example, if, inside you .zip file, your files looks like shapefile/xxxxxxx.shp, the .zip file cannot be uploaded.
        Inside your .zip file, it must looks like this xxxxxxxx.shp, xxxxxxxx.dbf, etc.

        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefiles
    :param store_name: the name of datastore in which you would like to upload the shapefiles
    :param folder_path: the local path to your shapefiles
    :param configure: this parameter takes three possible values
        first—(Default) Only setup the first feature type available in the data store.
        none—Do not configure any feature types.
        all—Configure all feature types.

    """
    shp_files = glob.glob(f"{folder_path}/*.shp")
    for f in shp_files:
        upload_shapefile(workspace_name, store_name, f, configure)
        print(f)
    zip_files = glob.glob(f"{folder_path}/*.zip")
    for f in zip_files:
        upload_shapefile(workspace_name, store_name, f, configure)
        print(f)
    return "Done"


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
def upload_raster(
    workspace_name,
    store_name,
    file_path,
    coverage_name=None,
    file_fmt="geotiff",
    configure="all",
):
    """Upload a local raster into geoserver.
        Only one raster is allowed per coverage store unless using raster mosaic.

    :param workspace_name: the name of workspace
    :param store_name: the name of data store
    :param file_path: the local file path to the raster(.zip)
    :param coverage_name: The coverageName parameter specifies the name of the coverage within the coverage store.
        This parameter is only relevant if the configure parameter is not equal to “none”.
        If not specified the resulting coverage will receive the same name as its containing coverage store.
    :param file_fmt: "geotiff" -- GeoTIFF
                     "worldimage" -- Georeferenced image (JPEG, PNG, TIFF)
                     "imagemosaic" -- Image mosaic
    :param configure: this parameter takes three possible values
        "first" —- (Default) Only setup the first feature type available in the data store.
        "none"  —- Do not configure any feature types.
        "all"   —- Configure all feature types.

    """
    file_fmt_ = file_fmt

    p = Path(file_path)
    ext = p.suffix
    if ext in [".tif", ".tiff"]:
        content_type = "image/tiff"
        file_fmt_ = "geotiff"
    elif ext in [".jpg", ".jpeg"]:
        content_type = "image/jpeg"
        file_fmt_ = "worldimage"
    elif ext in [".png"]:
        content_type = "image/png"
        file_fmt_ = "worldimage"
    elif ext in [".zip"]:
        content_type = "application/zip"
    else:
        raise Exception(f"unsupported file format: {ext}")

    headers = {"content-type": content_type, "Accept": "application/json"}

    coverage_name_ = coverage_name if coverage_name else store_name
    url = (
        f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/"
        + f"file.{file_fmt_}?coverageName={coverage_name_}&configure={configure}"
    )
    with open(file_path, "rb") as f:
        r = requests.put(
            url, data=f.read(), auth=(a.username, a.passwd), headers=headers
        )

        if r.status_code in [200, 201]:
            print(f"Raster {file_path} has been uploaded successfully")
        else:
            print(
                f"Unable to upload raster {file_path}. Status code: {r.status_code}, { r.content}"
            )
        return r


def upload_raster_folder(workspace_name, folder_path, file_fmt="geotiff"):
    """Upload all the rasters within a local folder.
        The rasters can be .zip, .tiff, .tif, .png, .jpg, .jpeg files.
        Make sure you have georeferenced your rasters.
        The store name and layer name will be deduced from file name.

    :param workspace_name: the name of destine workspace in which you would like to
        upload the rasters
    :param folder_path: the local path to your rasters
    :param file_fmt: "geotiff" -- GeoTIFF
                     "worldimage" -- Georeferenced image (JPEG, PNG, TIFF)
                     "imagemosaic" -- Image mosaic

    """
    for file_ext in [".zip", ".tiff", ".tif", ".png", ".jpg", ".jpeg"]:
        raster_files = glob.glob(f"{folder_path}/*{file_ext}")
        for f in raster_files:
            p = Path(f)
            upload_raster(
                workspace_name,
                Path(f).stem.split(".")[0],
                f,
                file_fmt=file_fmt,
                configure="all",
            )
            print(f)
    return "Done"


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


@auth
def publish_raster_layer(workspace_name, store_name, layer_name):
    """Publish a coverage/raster layer from a coverage store.
        It seems ,for some reason, that only one raster is allowed per coverage store.

    :param workspace_name: the name of the workspace
    :param store_name: the name of the coverage store in which the raster layer reside
    :param layer_name: the name of the raster layer

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/coverages/"

    layer_xml = f"<coverage><name>{layer_name}</name><nativeName>{layer_name}</nativeName></coverage>"
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
def add_style(style_name, workspace=None):
    """Add an empty style globally or into a workspace.

    :param style_name: the name of the style which you would like to create
    :param workspace:  (Default value = None) the name of the workspace.
        If the workspace name is not given, the new style will be a global one.

    """
    # a.username, a.passwd, a.server_url = get_cfg()
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{a.server_url}/rest/styles/"

    style_xml = (
        f"<style><name>{style_name}</name><filename>{style_name}.sld</filename></style>"
    )
    headers = {"content-type": "text/xml"}
    r = requests.post(
        url=url, data=style_xml, auth=(a.username, a.passwd), headers=headers
    )
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
    # a.username, a.passwd, a.server_url = get_cfg()

    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{a.server_url}/rest/styles"

    header = {"content-type": "application/vnd.ogc.sld+xml"}
    # SLD 1.1 / SE 1.1 with a mime type of application/vnd.ogc.se+xml
    # SLD package(zip file containing sld and image files used in the style) with a mime type of application/zip

    payload = {"name": style_name, "raw": "true"}

    with open(file_path, "r") as f:
        style_data = f.read()
        r = requests.post(
            url,
            data=style_data,
            auth=(a.username, a.passwd),
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
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{a.server_url}/rest/styles/{style_name}"

    header = {"content-type": "application/vnd.ogc.sld+xml"}

    r = requests.put(
        url,
        data=style_data,
        auth=(a.username, a.passwd),
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
    # a.username, a.passwd, a.server_url = get_cfg()

    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles/{style_name}"
    else:
        url = f"{a.server_url}/rest/styles/{style_name}"

    r = requests.delete(
        url, auth=(a.username, a.passwd), params={"recurse": True, "purge": True}
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
    # a.username, a.passwd, a.server_url = get_cfg()

    headers = {"content-type": "application/json"}
    # headers = {"content-type": "text/xml"}
    url = f"{a.server_url}/rest/layers/{full_layer_name}"
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
        auth=(a.username, a.passwd),
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
    # a.username, a.passwd, a.server_url = get_cfg()
    url = f"{a.server_url}/rest/layers/{full_layer_name}"

    headers = {"content-type": "text/xml"}
    r = requests.put(
        url,
        data=f"<layer><styles><style><name>{full_style_name}</name></style></styles></layer>",
        auth=(a.username, a.passwd),
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
    payload = {"recurse": "true", "quietOnNotFound": "true"}

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
def get_styles(workspace=None):
    """Get all global styles or all styles in a workspace

    :param workspace:  (Default value = None) If the workspace name is not given,
        all global styles will be returned.

    """
    if workspace:
        url = f"{a.server_url}/rest/workspaces/{workspace}/styles"
    else:
        url = f"{a.server_url}/rest/styles"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
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
    url = f"{a.server_url}/rest/workspaces"
    r = requests.get(
        url,
        auth=(a.username, a.passwd),
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
    url = f"{a.server_url}/rest/workspaces/{name}"
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
