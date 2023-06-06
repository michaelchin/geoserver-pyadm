#!/bin/bash
set -e
GEOSERVER_PYADM_TEST_MODULE=true

#pip install -y geoserver-pyadm

python test_create_workspace.py
python test_delete_workspace.py

python test_upload_local_raster.py clean
python test_upload_geopackage.py clean
python test_publish_shapefiles_on_server.py clean