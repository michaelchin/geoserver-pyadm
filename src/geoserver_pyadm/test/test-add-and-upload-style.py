TEST_MODULE = False

if TEST_MODULE:
    from geoserver_pyadm import geoserver
else:
    # if you are testing the local geoserver.py, use the code below
    import sys
    sys.path.append('../')
    import geoserver

ws_name = "a-test-workspace"

r = geoserver.add_style("test-style-0")
print(r)
r = geoserver.add_style("test-style-1", ws_name)
print(r)
r = geoserver.add_style("test-style-2", ws_name)
print(r)

r = geoserver.upload_style("test-style-3", f"test.sld")
print(r)
r = geoserver.upload_style("test-style-4", f"test.sld", ws_name)
print(r)
