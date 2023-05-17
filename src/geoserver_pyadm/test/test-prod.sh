#!/bin/bash
set -e
GEOSERVER_PYADM_TEST_MODULE=true

#pip install -y geoserver-pyadm

python test-create-workspace.py
python test-delete-workspace.py

python test-upload-local-raster.py clean
python test-upload-geopackage.py clean