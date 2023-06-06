#!/bin/bash

#assume the working directory is the root of this repository

pip3 install build twine
python -m build
twine check dist/*

pip3 install pip-tools
pip3 install -U sphinx
pip-compile pyproject.toml
pip3 install .
rm doc/source/geoserver_pyadm.rst
rm doc/source/modules.rst
sphinx-apidoc -o doc/source src/geoserver_pyadm/
cd doc
make html