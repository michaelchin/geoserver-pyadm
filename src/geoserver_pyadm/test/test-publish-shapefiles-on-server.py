import sys
from importer import *

ws_name_1 = "test-workspace-1"
store_name_1 = "test-store-1"
ws_name_2 = "test-workspace-2"
store_name_2 = "test-store-2"

r = geoserver.create_workspace(ws_name_1)
r = geoserver.create_workspace(ws_name_2)

# configure="none", upload local shapefiles only, the new layers will be published in next function call
r = geoserver.upload_shapefile(
    ws_name_1, store_name_1, f"shapefiles/coastline-0-Ma-test.zip", "none"
)

# publish the layers
r = geoserver.publish_layer(ws_name_1, store_name_1, "coastline-0-Ma-test")
print(r)

# create a store from a folder on geoserver(relative path to "data_dir")
# the folder and files were uploaded via code above
# and publish a layer from one of the shapefiles in the folder
r = geoserver.create_datastore(
    ws_name_2, store_name_2, f"data/{ws_name_1}/{store_name_1}"
)
print(r)
r = geoserver.publish_layer(ws_name_2, store_name_2, "coastline-0-Ma-test")
print(r)

if len(sys.argv) > 1:
    print(sys.argv[1])
    if sys.argv[1] == "clean":
        geoserver.delete_workspace(ws_name_1)
        geoserver.delete_workspace(ws_name_2)
