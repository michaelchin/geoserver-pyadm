import os

GEOSERVER_PYADM_TEST_MODULE = False
if 'GEOSERVER_PYADM_TEST_MODULE' in os.environ and os.environ['GEOSERVER_PYADM_TEST_MODULE'].lower() == 'true':
    GEOSERVER_PYADM_TEST_MODULE = True

if GEOSERVER_PYADM_TEST_MODULE:
    from geoserver_pyadm import geoserver
    print('GEOSERVER_PYADM_TEST_MODULE=true; testing geoserver_pyadm module')
else:
    # if you are testing the local geoserver.py, use the code below
    import sys
    sys.path.append('../')
    import geoserver
    print('GEOSERVER_PYADM_TEST_MODULE=false; testing geoserver.py')
