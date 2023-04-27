# geoserver-pyadm

#### activate/deactivate the python virtual env

`source python-venv/bin/activate`

`~ deactivate`

#### build the package

- `pip3 install pip-tools`
- `pip-compile pyproject.toml`
- `pip3 install .`