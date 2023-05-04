from importer import *

ws_name = "a-test-workspace"
store_name_1 = "a-test-store_1"

geoserver.create_workspace(ws_name)

# upload local shapefiles, the new layers will be published
r = geoserver.upload_shapefiles(ws_name, store_name_1,
                                f"coastlines_0Ma.zip")
print(r)
r = geoserver.upload_shapefiles(
    ws_name, store_name_1, f"coastlines_230Ma.zip"
)
print(r)
