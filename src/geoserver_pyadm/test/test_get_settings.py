from importer import *

r = geoserver.get_global_settings()
print(r)

r = geoserver.get_status()
print(r)

r = geoserver.get_version()
print(r)
