from importer import *

ws_name = "a-test-workspace"
store_name = "tiger_roads"
r = geoserver.delete_layer(store_name)
print(r)
