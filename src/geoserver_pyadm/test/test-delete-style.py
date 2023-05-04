from importer import *

ws_name = "a-test-workspace"

geoserver.delete_style("test-style-0")
# also work without workspace name, strange?
geoserver.delete_style("test-style-1", ws_name)
