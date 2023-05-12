from importer import *

r = geoserver.delete_workspace("my-test-workspace", quiet_on_not_exist=False)
print(r)
