from importer import *

ws_name = "MULLER2019-test"

r = geoserver.get_coverage_stores(ws_name)
print(r)

r = geoserver.get_coverage_store_info(ws_name, "test-mosaic")
print(r)

"""
r = geoserver.reindex_existing_image_mosaic_store(
    ws_name,
    "test-mosaic",
    "file:///mnt/volume-1/geoserver/data_dir/data/MERDITH2021/paleoDEM-Merdith/",
)
print(r)


r = geoserver.add_raster_to_image_mosaic_store(
    ws_name,
    "test-mosaic",
    "file:///mnt/volume-1/geoserver/data_dir/data/MERDITH2021/paleoDEM-Merdith/agegrid_7777.tiff",
)
print(r)
"""
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

r = geoserver.upload_image_mosaic(ws_name, "test-mosaic", "rasters/temperature.zip")
print(r)

r = geoserver.create_coverage_store(
    ws_name,
    "test-coverage-store",
    "file:///mnt/volume-1/geoserver/data_dir/data/MERDITH2021/paleoDEM-Merdith/agegrid_7777.tiff",
)
