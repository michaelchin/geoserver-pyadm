from importer import *

ws_name = "test-workspace"
store_name = "test-paleodem"
geoserver_data_dir = "/mnt/volume-1/geoserver/data_dir"

geoserver.create_workspace(ws_name)

# configure="none" will not publish the layers
# configure="all" or "first" will publish the layers
# the main purpose of this function call is upload the .nc files
r = geoserver.upload_image_mosaic(
    ws_name, store_name, "rasters/paleodem.zip", configure="none"
)
print(r)

# create an empty store
r = geoserver.upload_image_mosaic(
    ws_name,
    store_name + "-empty",
    "rasters/paleodem-without-nc-files.zip",
    configure="none",
)
print(r)

r = geoserver.imagemosaic.reindex_existing_image_mosaic_store(
    ws_name,
    store_name + "-empty",
    f"file://{geoserver_data_dir}/data/{ws_name}/{store_name}/",
)
print(r)

r = geoserver.get_coverages(ws_name, store_name + "-empty")
print(r.content)
