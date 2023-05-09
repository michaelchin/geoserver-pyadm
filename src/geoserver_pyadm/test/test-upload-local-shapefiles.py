from importer import *

ws_name_1 = "a-test-workspace-1"
ws_name_2 = "a-test-workspace-2"
store_name_1 = "a-test-store-1"
store_name_2 = "a-test-store-2"

geoserver.create_workspace(ws_name_1)
geoserver.create_workspace(ws_name_2)

# configure="none", upload local shapefiles only, the new layers will be published in next function call
r = geoserver.upload_shapefile(
    ws_name_1, store_name_1, f"shapefiles/coastline-0-Ma-test.zip", "none"
)
print(r)
r = geoserver.upload_shapefile(
    ws_name_1,
    store_name_1,
    f"shapefiles/Global_EarthByte_GPlates_PresentDay_ContinentalPolygons.shp",
    "none",
)
print(r)

# publish the layers
r = geoserver.publish_layer(ws_name_1, store_name_1, "coastline-0-Ma-test")
print(r)
r = geoserver.publish_layer(
    ws_name_1, store_name_1, "Global_EarthByte_GPlates_PresentDay_ContinentalPolygons"
)
print(r)


# use configure="all" to upload all shapefiles and publish them
# be aware, all the shapefiles in store_name_2 will be published(not only the ones you just uploaded)
r = geoserver.upload_shapefile_folder(ws_name_2, store_name_2, f"shapefiles", "all")
print(r)
