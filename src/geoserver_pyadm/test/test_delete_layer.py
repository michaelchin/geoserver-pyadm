from importer import *

# prepare test data first, create two layers
ws_name_1 = "a-test-workspace-1"
ws_name_2 = "a-test-workspace-2"
ws_name_3 = "a-test-workspace-3"
store_name_1 = "a-test-store-1"
store_name_2 = "a-test-store-2"
store_name_3 = "a-test-store-3"

geoserver.create_workspace(ws_name_1)
geoserver.create_workspace(ws_name_2)
geoserver.create_workspace(ws_name_3)

r = geoserver.upload_shapefile(
    ws_name_1, store_name_1, f"shapefiles/coastline-0-Ma-test.zip", "none"
)
r = geoserver.publish_layer(ws_name_1, store_name_1, "coastline-0-Ma-test")

r = geoserver.upload_shapefile(
    ws_name_2, store_name_2, f"shapefiles/coastline-0-Ma-test.zip", "none"
)
r = geoserver.publish_layer(ws_name_2, store_name_2, "coastline-0-Ma-test")
r = geoserver.upload_shapefile(
    ws_name_3, store_name_3, f"shapefiles/coastline-0-Ma-test.zip", "none"
)
r = geoserver.publish_layer(ws_name_3, store_name_3, "coastline-0-Ma-test")

# delete layer coastline-0-Ma-test in workspace ws_name_1
r = geoserver.delete_layer("coastline-0-Ma-test", ws_name_1)
# delete all coastline-0-Ma-test layers
r = geoserver.delete_layer("coastline-0-Ma-test")
print(r)
