# import functions into __init__.py

__version__ = "1.0.1"

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
    upload_geopackage,
    upload_geopackage_zip,
    upload_image_mosaic,
)

from .info import get_global_settings, get_status, get_version

from .layer import (
    get_layer,
    get_layer_styles,
    get_layers,
    publish_layer,
    publish_raster_layer,
    delete_layer,
    publish_geopackage_layer,
)

from .datastore import (
    get_datastores,
    create_datastore,
    delete_datastore,
    create_geopackage_store,
)

from .style import (
    get_styles,
    modify_style,
    add_additional_style,
    add_style,
    delete_style,
    set_default_style,
)

from .coveragestore import (
    get_coverage_stores,
    get_coverage_store_info,
    delete_coverage_store,
    create_coverage_store,
    create_coverage,
    get_coverages,
)

from . import imagemosaic
