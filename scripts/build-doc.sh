#!/bin/bash

source ./geoserver-pyadm-venv/bin/activate

pip-compile pyproject.toml
pip3 install .
rm doc/source/geoserver_pyadm.rst
rm doc/source/modules.rst
sphinx-apidoc -o doc/source src/geoserver_pyadm/
cd doc
make html