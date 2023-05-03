TEST_MODULE = False

if TEST_MODULE:
    from geoserver_pyadm import geoserver
else:
    # if you are testing the local geoserver.py, use the code below
    import sys
    sys.path.append('../')
    import geoserver

ws_name = "a-test-workspace"
store_name = "AgeGrid-0"
#
# upload the local raster zip file and the layer will be published
r = geoserver.upload_raster(
    ws_name,
    store_name,
    f"EarthByte_AREPS_Muller_etal_2016_AgeGrid-0.tiff.zip",
    "geotiff",
)
print(r)
