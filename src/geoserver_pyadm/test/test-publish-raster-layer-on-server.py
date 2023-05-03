# create a coverage store and publish it
TEST_MODULE = False

if TEST_MODULE:
    from geoserver_pyadm import geoserver
else:
    # if you are testing the local geoserver.py, use the code below
    import sys
    sys.path.append('../')
    import geoserver

ws_name = "a-test-workspace"
store_name = "a-test-coveragestore"
layer_name = "agegrid_9999"

r = geoserver.create_coveragestore(
    ws_name, store_name, "data/rasters/agegrid_9999.tif"
)
print(r)
r = geoserver.publish_raster_layer(ws_name, store_name, layer_name)
print(r)
