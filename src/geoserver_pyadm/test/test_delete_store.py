from importer import *

ws_name = "a-test-workspace"
store_name_1 = "a-test-store-1"
r = geoserver.delete_datastore(ws_name, store_name_1)
print(r)
