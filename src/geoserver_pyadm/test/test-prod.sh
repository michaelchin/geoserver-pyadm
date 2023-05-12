#!/bin/bash
set -e
GEOSERVER_PYADM_TEST_MODULE=true

python test-create-workspace.py
python test-delete-workspace.py
python test-upload-local-raster.py