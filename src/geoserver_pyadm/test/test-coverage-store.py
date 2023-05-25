from importer import *

ws_name = "MULLER2019-test"
store_name = "test-paleodem"
geoserver_data_dir = "/mnt/volume-1/geoserver/data_dir"

"""
r = geoserver.get_coverage_stores(ws_name)
print(r)

r = geoserver.get_coverage_store_info(ws_name, "test-mosaic")
print(r)







r = geoserver.get_rasters_in_image_mosaic_store(ws_name, "test-mosaic", "test_mosaic")
print(r)

r = geoserver.delete_raster_from_image_mosaic_store(
    ws_name, "test-mosaic", "test_mosaic", "test_mosaic.13"
)
print(r)

r = geoserver.get_rasters_in_image_mosaic_store(ws_name, "test-mosaic", "test_mosaic")
print(r)

r = geoserver.delete_coverage_store(ws_name, "test-mosaic")
print(r)
"""

# configure="none" will not publish the layers
# configure="all" or "first" will publish the layers
# the main purpose of this function call is upload the .nc files
r = geoserver.upload_image_mosaic(
    ws_name, store_name, "rasters/paleodem.zip", configure="none"
)
print(r)

# create an empty store to do the add/delete testing
r = geoserver.upload_image_mosaic(
    ws_name,
    store_name + "-empty",
    "rasters/paleodem-without-nc-files.zip",
    configure="none",
)
print(r)

# add the .nc file in the first store to the empty store
r = geoserver.add_raster_to_image_mosaic_store(
    ws_name,
    store_name + "-empty",
    f"file://{geoserver_data_dir}/data/{ws_name}/{store_name}/20230101.test1.paleoDEM.nc",
)
print(r)

# create a new coverage for 20230101.test1.paleoDEM.nc(publish layer)
r = geoserver.create_coverage(ws_name, store_name + "-empty", "test1")
print(r)
r = geoserver.create_coverage(ws_name, store_name, "test5")
print(r)

# enable the time dimension for the layer
r = geoserver.enable_time_dimension(ws_name, store_name + "-empty", "test1")
print(r)

r = geoserver.get_rasters_in_image_mosaic_store(ws_name, store_name, "test5")
print(r)

# the ID can be found from the output of get_rasters_in_image_mosaic_store
r = geoserver.delete_raster_from_image_mosaic_store(
    ws_name, store_name, "test5", "test5.1"
)
print(r)

r = geoserver.get_rasters_in_image_mosaic_store(ws_name, store_name, "test5")
print(r)

r = geoserver.reindex_existing_image_mosaic_store(
    ws_name,
    store_name + "-empty",
    f"file://{geoserver_data_dir}/data/{ws_name}/{store_name}/",
)
print(r)

"""
r = geoserver.create_coverage_store(
    ws_name,
    "test-coverage-store",
    "file:///mnt/volume-1/geoserver/data_dir/data/MERDITH2021/paleoDEM-Merdith/agegrid_7777.tiff",
)

r = geoserver.upload_image_mosaic(ws_name, "test-gome", "rasters/gome2.zip")
print(r)

r = geoserver.add_raster_to_image_mosaic_store(
    ws_name,
    "test-gome",
    "file:///mnt/volume-1/geoserver/data_dir/data/rasters/20130101.METOPA.GOME2.test.PGL.nc",
)
r = geoserver.add_raster_to_image_mosaic_store(
    ws_name,
    "test-gome",
    "file:///mnt/volume-1/geoserver/data_dir/data/rasters/20130101.METOPA.GOME2.CF.PGL.nc",
)
r = geoserver.add_raster_to_image_mosaic_store(
    ws_name,
    "test-gome",
    "file:///mnt/volume-1/geoserver/data_dir/data/rasters/20130101.METOPA.GOME2.BrO.PGL.nc",
)
print(r)

r = geoserver.create_coverage(ws_name, "test-gome", "test")
print(r)

r = geoserver.enable_time_dimension(ws_name, "test-gome", "test")
print(r)
"""
