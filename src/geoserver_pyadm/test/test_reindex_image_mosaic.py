from importer import *

# it is difficult to automate this test case. you need to do something manually. Read the comments below.

ws_name = "test-workspace"
store_name = "test-mosaic"
reindex_store_name = "test-mosaic-reindex"
store_zip = "rasters/temperature.zip"
reindex_store_zip = "rasters/temperature-with-one-tiff-file.zip"
# you need to change this data_dir according to your geoserver setup
geoserver_data_dir = "/mnt/volume-1/geoserver/data_dir"

geoserver.create_workspace(ws_name)

# configure="none" will not publish the layers
# configure="all" or "first" will publish the layers
# the main purpose of this function call is upload the .tiff files
r = geoserver.upload_image_mosaic(ws_name, store_name, store_zip, configure="none")
print(r)

# create a store with only one tiff file(empty store is not allowed here)
# the paleodem.zip allows empty store. The configuration is in paleodem.xml.
r = geoserver.upload_image_mosaic(
    ws_name,
    reindex_store_name,
    reindex_store_zip,
    configure="none",
)
print(r)

# reindex the image mosaic store with the .tiff files in other folder
r = geoserver.imagemosaic.reindex_image_mosaic_store(
    ws_name,
    reindex_store_name,
    f"file://{geoserver_data_dir}/data/{ws_name}/{store_name}/",
)
print(r)

# find the coverage names. Here it should return just one name.
r = geoserver.get_available_coverage_names(ws_name, reindex_store_name)
print(r)

# create a coverage(publish the layer)
r = geoserver.create_coverage(ws_name, reindex_store_name, r[0])
print(r)

# get all granules in a coverage within an image mosaic store
r = geoserver.imagemosaic.get_rasters_in_coverage(
    ws_name, reindex_store_name, reindex_store_name
)
print(r)

if len(sys.argv) > 1:
    print(sys.argv[1])
    if sys.argv[1] == "clean":
        geoserver.delete_workspace(ws_name)
    # you also need to remove the folders file://{geoserver_data_dir}/data/{ws_name}/{store_name}/
    # and file://{geoserver_data_dir}/data/{ws_name}/{reindex_store_name}/
