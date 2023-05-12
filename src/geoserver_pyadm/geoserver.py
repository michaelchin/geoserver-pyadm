"""
Geoserver Python API
"""
from .workspace import (
    create_workspace,
    delete_workspace,
    get_all_workspaces,
    get_workspace,
)

from .upload import (
    upload_raster,
    upload_raster_folder,
    upload_shapefile,
    upload_shapefile_folder,
    upload_shapefile_zip,
    upload_style,
)

from .info import get_global_settings, get_status, get_version

from .layer import get_layer, get_layer_styles, get_layers

from .datastore import get_datastores, create_coveragestore, create_store, delete_store

from .style import (
    get_styles,
    modify_style,
    add_additional_style,
    add_style,
    delete_style,
    set_default_style,
)
