import sys
from importer import *

ws_name_1 = "test-workspace-1"
store_name_1 = "test-store-1"
ws_name_2 = "test-workspace-2"
store_name_2 = "test-store-2"
ws_name_3 = "test-workspace-3"
store_name_3 = "test-store-3"

r = geoserver.create_workspace(ws_name_1)
r = geoserver.create_workspace(ws_name_2)
r = geoserver.create_workspace(ws_name_3)

# make sure you have unzip installed
os.system(
    "unzip -o geopackage/shapes_static_polygons_Merdith_et_al.gpkg.zip -d geopackage"
)

# test upload zipped geopackage
# configure="none", upload local shapefiles only, the new layers will be published in next function call
r = geoserver.upload_geopackage_zip(
    ws_name_1,
    store_name_1,
    f"geopackage/shapes_static_polygons_Merdith_et_al.gpkg.zip",
    "none",
)

# publish the layers
r = geoserver.publish_geopackage_layer(
    ws_name_1, store_name_1, "shapes_static_polygons_Merdith_et_al", "polygon"
)
print(r)

# *************************************************************************

# test upload .gpkg directly
r = geoserver.upload_geopackage(
    ws_name_2,
    store_name_2,
    f"geopackage/shapes_static_polygons_Merdith_et_al.gpkg",
    "none",
)
print(r.content)

# publish the layers
r = geoserver.publish_geopackage_layer(
    ws_name_2, store_name_2, "shapes_static_polygons_Merdith_et_al", "polygon"
)
print(r)

# **********************************************************************************

# create a store from a folder on geoserver(relative path to "data_dir")
# the folder and files were uploaded via code above
# and publish a layer from one of the geopackage in the folder
r = geoserver.create_geopackage_store(
    ws_name_3,
    store_name_3,
    f"data/{ws_name_1}/{store_name_1}/shapes_static_polygons_Merdith_et_al.gpkg",
)
print(r)
r = geoserver.publish_geopackage_layer(
    ws_name_3, store_name_3, "shapes_static_polygons_Merdith_et_al", "polygon"
)
print(r)

if len(sys.argv) > 1:
    print(sys.argv[1])
    if sys.argv[1] == "clean":
        geoserver.delete_workspace(ws_name_1)
        geoserver.delete_workspace(ws_name_2)
        geoserver.delete_workspace(ws_name_3)
        os.system("rm -rf geopackage/shapes_static_polygons_Merdith_et_al.gpkg")
