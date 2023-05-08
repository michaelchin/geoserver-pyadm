from importer import *

ws_name = "a-test-workspace"
store_name = "a-test-store"

geoserver.create_workspace(ws_name)

# upload local shapefiles, the new layers will be published
"""
r = geoserver.upload_shapefile(ws_name, store_name, f"shapefiles/coastlines_0Ma.zip")
print(r)
r = geoserver.upload_shapefile(ws_name, store_name, f"shapefiles/coastlines_230Ma.zip")
print(r)
r = geoserver.upload_shapefile(
    ws_name,
    store_name,
    f"shapefiles/Global_EarthByte_GPlates_PresentDay_ContinentalPolygons.shp",
)
print(r)
"""

geoserver.upload_shapefile_folder(ws_name, store_name, f"shapefiles")
