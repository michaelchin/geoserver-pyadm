from importer import *


def print_sep(msg, limit=120):
    if len(msg) > limit:
        print(msg)
    else:
        stars = "*" * int((limit - len(msg)) / 2)
        print(f"\n{stars}{msg}{stars}")


ws_name = "a-test-workspace"

print_sep(f"get all workspaces")
r = geoserver.get_all_workspaces()
print(r)

print_sep(f"get workspace info {ws_name}")
r = geoserver.get_workspace(ws_name)
print(r)

print_sep(f"get datastores in workspace:{ws_name}")
r = geoserver.get_datastores(ws_name)
print(r)

# get styles associated with a layer
print_sep(f"get styles in layer {ws_name}:giant_polygon")
r = geoserver.get_layer_styles(f"{ws_name}:giant_polygon")
print(r)

print_sep(f"get layer info {ws_name}:tiger_roads")
r = geoserver.get_layer("tiger_roads", ws_name)
print(r)

print_sep(f"get layer info tiger_roads")
r = geoserver.get_layer("tiger_roads")
print(r)

print_sep(f"get all layers in workspace: {ws_name}")
r = geoserver.get_layers(ws_name)
print(r)

print_sep(f"get all layers")
r = geoserver.get_layers()
print(f"{len(r)} layers found!")

print_sep(f"get global styles")
r = geoserver.get_styles()
print(r)

print_sep(f"get all styles in workspace: {ws_name}")
r = geoserver.get_styles(ws_name)
print(r)

print()
