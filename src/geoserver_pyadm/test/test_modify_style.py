from importer import *

ws_name = 'a-test-workspace'

geoserver.add_style("test-style-0")
geoserver.add_style("test-style-1", ws_name)

with open('test.sld', "r") as f:
    style_data = f.read()
    r = geoserver.modify_style("test-style-0", style_data)
    print(r)
    r = geoserver.modify_style("test-style-1", style_data, ws_name)
    print(r)
