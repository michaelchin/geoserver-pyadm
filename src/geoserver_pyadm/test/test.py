import os, sys

sys.path.insert(0, "../")  # make sure the geoserver.py is in the ../
import geoserver

script_path = os.path.dirname(os.path.realpath(__file__))

ws_name = "a-test-workspace"
store_name_1 = "a-test-store_1"
store_name_2 = "a-test-store_2"
store_name_3 = "a-test-store_3"
store_name_4 = "a-test-store_4"

geoserver.delete_workspace(ws_name)

geoserver.create_workspace(ws_name)

# upload local shapefiles
geoserver.upload_shapefiles(ws_name, store_name_1, f"{script_path}/coastlines_0Ma.zip")
geoserver.upload_shapefiles(
    ws_name, store_name_1, f"{script_path}/coastlines_230Ma.zip"
)

# create a store from a folder on geoserver(relative path to "data_dir")
# and publish a layer from one of the shapefiles in the folder
geoserver.create_store(ws_name, store_name_2, "data/nyc")
geoserver.publish_layer(ws_name, store_name_2, "tiger_roads")
geoserver.publish_layer(ws_name, store_name_2, "giant_polygon")


#
# upload rasters
geoserver.upload_raster(
    ws_name,
    "AgeGrid-0",
    f"{script_path}/EarthByte_AREPS_Muller_etal_2016_AgeGrid-0.tiff.zip",
    "geotiff",
)
geoserver.upload_raster(
    ws_name,
    "AgeGrid-230",
    f"{script_path}/EarthByte_AREPS_Muller_etal_2016_AgeGrid-230.tiff.zip",
    "geotiff",
)

# create a coverage store and publish it
geoserver.create_coveragestore(
    ws_name, store_name_4, "data/rasters/agegrid_2017111319.tif"
)
geoserver.publish_raster_layer(ws_name, store_name_4, "agegrid_2017111319")

#
geoserver.delete_style("test-style-0")
geoserver.delete_style("test-style-1")
geoserver.add_style("test-style-0")
geoserver.add_style("test-style-1", ws_name)
geoserver.upload_style("test-style-0", f"{script_path}/test.sld")
geoserver.upload_style("test-style-1", f"{script_path}/test.sld", ws_name)


geoserver.set_default_style(f"{ws_name}:tiger_roads", "test-style-0")
geoserver.add_additional_style(f"{ws_name}:giant_polygon", f"{ws_name}:test-style-1")

geoserver.get_styles(f"{ws_name}:giant_polygon")
geoserver.get_layer("tiger_roads", ws_name)
