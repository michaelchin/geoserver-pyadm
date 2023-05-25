import glob
import json
import os
import tempfile
import zipfile
from pathlib import Path

import requests

from . import _auth as a
from ._auth import auth


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

    p = Path(file_path)
    ext = p.suffix
    if ext in [".tif", ".tiff"]:
        # content_type = "image/tiff"
        file_fmt_ = "geotiff"
    elif ext in [".jpg", ".jpeg"]:
        # content_type = "image/jpeg"
        file_fmt_ = "worldimage"
    elif ext in [".png"]:
        # content_type = "image/png"
        file_fmt_ = "worldimage"
    elif ext in [".zip"]:
        file_fmt_ = file_fmt
        # content_type = "application/zip"
    else:
        raise Exception(f"unsupported file format: {ext}")

    content_type = "application/zip"
    headers = {"content-type": content_type, "Accept": "application/json"}

    coverage_name_ = coverage_name if coverage_name else store_name
    url = (
        f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/"
        + f"file.{file_fmt_}?coverageName={coverage_name_}&configure={configure}"
    )
    if ext != ".zip":
        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(
                f"{tmp_dir}/{p.stem}.zip",
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            ) as tmp_zip:
                tmp_zip.write(file_path, os.path.basename(file_path))
            with open(f"{tmp_dir}/{p.stem}.zip", "rb") as f:
                r = requests.put(
                    url,
                    data=f.read(),
                    auth=(a.username, a.passwd),
                    headers=headers,
                )
    else:
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
def upload_zip(workspace_name, store_name, file_path, format="shp", configure="none"):
    """Upload a local .zip file which contains shapefile.
        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefile
    :param store_name: the name of datastore in which you would like to upload the shapefile
    :param file_path: the local file path to your shapefile(.zip)
    :param format: support 'shp' and 'gpkg'
    :param configure: this parameter takes three possible values
        "first" —- (Default) Only setup the first feature type available in the data store.
        "none"  —- Do not configure any feature types.
        "all"   —- Configure all feature types.

    """
    headers = {
        "Content-type": "application/zip",
        "Accept": "application/xml",
    }

    file_name = Path(file_path).stem
    url = (
        f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"
        + f"/{store_name}/file.{format}?filename={file_name}&update=overwrite&configure={configure}"
    )

    with open(file_path, "rb") as f:
        r = requests.put(
            url,
            data=f.read(),
            auth=(a.username, a.passwd),
            headers=headers,
        )
    return r


def upload_geopackage_zip(workspace_name, store_name, file_path, configure="none"):
    """Upload a local .zip file which contains geopackage file.
        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefile
    :param store_name: the name of datastore in which you would like to upload the shapefile
    :param file_path: the local file path to your geopackage(.zip)
    :param configure: this parameter takes three possible values
        "first" —- (Default) Only setup the first feature type available in the data store.
        "none"  —- Do not configure any feature types.
        "all"   —- Configure all feature types.

    """
    r = upload_zip(workspace_name, store_name, file_path, "gpkg", configure)

    # it seems there is bug in geoserver 2.21
    # I have to update the "database" path to make the store valid
    headers = {
        "Content-type": "application/json",
    }

    cfg = {
        "dataStore": {
            "name": store_name,
            "type": "GeoPackage",
            "connectionParameters": {
                "entry": [
                    {
                        "@key": "database",
                        "$": f"file:data/{workspace_name}/{store_name}/{os.path.basename(file_path)[:-4]}",
                    },
                    {"@key": "dbtype", "$": "geopkg"},
                ]
            },
        }
    }

    url = f"{a.server_url}/rest/workspaces/{workspace_name}/datastores/{store_name}/"

    requests.put(
        url,
        data=json.dumps(cfg),
        auth=(a.username, a.passwd),
        headers=headers,
    )
    return r


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
    return upload_zip(workspace_name, store_name, file_path, "shp", configure)


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
            with zipfile.ZipFile(
                f"{tmp_dir}/{file_name}.zip",
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            ) as tmp_zip:
                for f in files:
                    tmp_zip.write(f, os.path.basename(f))

            return upload_shapefile_zip(
                workspace_name, store_name, f"{tmp_dir}/{file_name}.zip", configure
            )
    else:
        raise Exception(f"Unsupported file extension: {file_path}")


def upload_geopackage(workspace_name, store_name, file_path, configure="none"):
    """Upload a local geopackage file.

        warning: when use configure="all", all the shapefiles in the datastore will
        be published(not only the one you just uploaded)

    :param workspace_name: the name of destine workspace in which you would like to
        upload the shapefile
    :param store_name: the name of datastore in which you would like to upload the shapefile
    :param file_path: the local path to your geopackge file
    :param configure: this parameter takes three possible values
        first—(Default) Only setup the first feature type available in the data store.
        none—Do not configure any feature types.
        all—Configure all feature types.

    """
    p = Path(file_path)
    file_name = p.stem
    ext = p.suffix

    if ext == ".zip":
        return upload_zip(workspace_name, store_name, file_path, "gpkg", configure)
    elif ext == ".gpkg":
        """
        # upload geopackage file without compression
        headers = {
            "Content-type": "application/x-sqlite3",
            "Accept": "application/xml",
        }

        url = (
            f"{a.server_url}/rest/workspaces/{workspace_name}/datastores"
            + f"/{store_name}/file.gpkg?filename={file_name}{ext}&update=overwrite&configure={configure}"
        )

        with open(file_path, "rb") as f:
            r = requests.put(
                url,
                data=f.read(),
                auth=(a.username, a.passwd),
                headers=headers,
            )"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            files = glob.glob(f"{file_path[:-5]}.*")
            with zipfile.ZipFile(
                f"{tmp_dir}/{file_name}{ext}.zip",
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            ) as tmp_zip:
                for f in files:
                    tmp_zip.write(f, os.path.basename(f))
            return upload_geopackage_zip(
                workspace_name,
                store_name,
                f"{tmp_dir}/{file_name}{ext}.zip",
                configure,
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
def upload_image_mosaic(workspace_name, store_name, file_path, configure="none"):
    """Upload a zip file which contains image mosaic configuration files, such as indexer.xml, datastore.properties,etc
    The zip file may also contains the .nc files. See test/rasters/paleodem.zip for example.
    A new image mosaic store will be created if everything goes well.

    :param workspace_name: workspace name
    :param store_name: coverage store name
    :param file_path: the location of the local .zip file
    :param configure: this parameter takes three possible values
        "first" —- (Default) Only setup the first feature type available in the data store.
        "none"  —- Do not configure any feature types.
        "all"   —- Configure all feature types.
    """
    headers = {
        "Content-type": "application/zip",
        "Accept": "application/json",
    }
    params = {"configure": configure}
    url = f"{a.server_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/file.imagemosaic"

    with open(file_path, "rb") as f:
        r = requests.put(
            url,
            data=f.read(),
            params=params,
            auth=(a.username, a.passwd),
            headers=headers,
        )
    if r.status_code in [200, 201]:
        print(f"Image mosaic store {store_name} is created.")
    else:
        print(f"Failed to create image mosaic store {store_name}.")
    return r
