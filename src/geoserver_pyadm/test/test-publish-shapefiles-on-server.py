from importer import *

ws_name = "a-test-workspace"
store_name_2 = "a-test-store-2"

r = geoserver.create_workspace(ws_name)
print(r)

# create a store from a folder on geoserver(relative path to "data_dir")
# and publish a layer from one of the shapefiles in the folder
r = geoserver.create_store(ws_name, store_name_2, "data/nyc")
print(r)
r = geoserver.publish_layer(ws_name, store_name_2, "tiger_roads")
print(r)
r = geoserver.publish_layer(ws_name, store_name_2, "giant_polygon")
print(r)
