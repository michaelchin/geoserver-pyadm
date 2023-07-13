from importer import *

# create a coverage store and publish it
ws_name = "a-test-workspace"
store_name = "a-test-coveragestore"
layer_name = "agegrid_9999d"

r = geoserver.create_workspace(ws_name, quiet_on_exist=True)

r = geoserver.create_coverage_store(
    ws_name, store_name, "data/rasters/agegrid_9999.tif"
)
print(r)

r = geoserver.publish_raster_layer(ws_name, store_name, layer_name)
# r = geoserver.publish_raster_layer(ws_name, store_name, layer_name, "agegrid_9999")
print(r)
