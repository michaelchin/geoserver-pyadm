import os
from importer import *

ws_name_1 = "test-workspace-1"
ws_name_2 = "test-workspace-2"
store_name_1 = "AgeGrid-0"
store_name_2 = "AgeGrid-230"

geoserver.create_workspace(ws_name_1)
geoserver.create_workspace(ws_name_2)

# make sure you have unzip installed
os.system(
    "unzip rasters/EarthByte_AREPS_Muller_etal_2016_AgeGrid-0.tiff.zip -d rasters"
)

# upload the local raster zip file
r = geoserver.upload_raster(
    ws_name_1,
    store_name_1,
    f"rasters/EarthByte_AREPS_Muller_etal_2016_AgeGrid-0.tiff",
    coverage_name="agegrid_0",
    file_fmt="geotiff",
    configure="all",
)
print(r)

r = geoserver.upload_raster(
    ws_name_1,
    store_name_2,
    f"rasters/EarthByte_AREPS_Muller_etal_2016_AgeGrid-230.tiff.zip",
    coverage_name="agegrid_230",
    file_fmt="geotiff",
    configure="all",
)
print(r)

r = geoserver.upload_raster_folder(ws_name_2, "rasters")
print(r)
