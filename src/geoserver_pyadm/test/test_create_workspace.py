from importer import *

r = geoserver.create_workspace("my-test-workspace", quiet_on_exist=False)
print(r)
