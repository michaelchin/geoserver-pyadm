from importer import *

ws_name = "a-test-workspace"
store_name_1 = "a-test-store-1"
store_name_2 = "a-test-store-2"

r = geoserver.create_workspace(ws_name)
print(r)

# create a store from a folder on geoserver(relative path to "data_dir")
# you can publish the layers in the folder later via web page or api
r = geoserver.create_datastore(ws_name, store_name_1, "data/nyc", is_dir=True)
print(r)

# create a store from a shapefile on geoserver(relative path to "data_dir")
# you can publish the shapefile layer later via web page or api
r = geoserver.create_datastore(ws_name, store_name_2, "data/shapefiles/states.shp")
print(r)
