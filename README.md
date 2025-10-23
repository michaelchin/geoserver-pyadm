# geoserver-pyadm

![Build, Test and Doc](https://github.com/michaelchin/geoserver-pyadm/actions/workflows/build.yml/badge.svg)

A Python wrapper/helper of Geoserver REST API.

### Installation

`pip3 install geoserver-pyadm`

### How to use

You need to create a .env file in your current working directory first. see [the template](https://github.com/michaelchin/geoserver-pyadm/blob/main/src/geoserver_pyadm/env-template.txt).

```python
from geoserver_pyadm import geoserver

# list all workspaces
print(geoserver.get_all_workspaces())

# get details about a workspace
print(geoserver.get_workspace("gplates"))

# create a workspace
geoserver.create_workspace("test-workspace-123")

# delete a workspace by name
geoserver.delete_workspace("test-workspace-123")

# list all data stores in workspace "gplates"
print(geoserver.get_datastores("gplates"))

# list all coverage stores in workspace "gplates"
print(geoserver.get_coverage_stores("gplates"))
```
