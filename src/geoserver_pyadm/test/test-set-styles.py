from importer import *

ws_name = 'a-test-workspace'
store_name = 'a-test-store'
geoserver.create_store(ws_name, store_name, "data/nyc")
geoserver.publish_layer(ws_name, store_name, "tiger_roads")
geoserver.publish_layer(ws_name, store_name, "giant_polygon")

r = geoserver.set_default_style(f"{ws_name}:tiger_roads", "test-style-0")
print(r)
r = geoserver.add_additional_style(
    f"{ws_name}:giant_polygon", f"{ws_name}:test-style-1")
print(r)
