import os

GEOSERVER_PYADM_TEST_MODULE = False
if (
    "GEOSERVER_PYADM_TEST_MODULE" in os.environ
    and os.environ["GEOSERVER_PYADM_TEST_MODULE"].lower() == "true"
):
    GEOSERVER_PYADM_TEST_MODULE = True

if GEOSERVER_PYADM_TEST_MODULE:
    # from geoserver_pyadm import geoserver
    import geoserver_pyadm as geoserver

    print("GEOSERVER_PYADM_TEST_MODULE=true; testing geoserver_pyadm module")
else:
    # if you are testing the local geoserver.py, use the code below
    import sys

    # Important: you need to `pip uninstall -y geoserver-pyadm`
    sys.path.insert(0, "../..")
    from geoserver_pyadm import geoserver

    print("GEOSERVER_PYADM_TEST_MODULE=false; testing geoserver.py")
