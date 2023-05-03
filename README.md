# geoserver-pyadm

#### activate/deactivate the python virtual env

- `source geoserver-pyadm-venv/bin/activate`

- `deactivate`

#### build and install the package

- `pip3 install pip-tools`
- `pip-compile pyproject.toml`
- `pip3 install .`

#### test

- .env must be in current working directory or the env variables have been set.