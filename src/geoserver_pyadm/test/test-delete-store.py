TEST_MODULE = False

if TEST_MODULE:
    from geoserver_pyadm import geoserver
else:
    # if you are testing the local geoserver.py, use the code below
    import sys
    sys.path.append('../')
    import geoserver

ws_name = "a-test-workspace"
store_name_1 = "a-test-store-1"
r = geoserver.delete_store(ws_name, store_name_1)
print(r)
