#!/usr/bin/env python
import os
import re
import sys

from dotenv import load_dotenv
from geo.Geoserver import Geoserver

# server_url = "https://geosrv.gplates.org/geoserver/"
# workspace_name = "MULLER2019"
# name_patten = r"^paleo-age-grid-(\d+)-Ma$"

script_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(f"{script_path}/.env")  # take environment variables from .env.

# get all layer names from a workspace
def get_layers(workspace=""):
    layers = geo.get_layers()["layers"]["layer"]
    ret = []
    if len(workspace) == 0:
        for layer in layers:
            ret.append(layer["name"].split(":")[1])
    else:
        for layer in layers:
            if layer["name"].startswith(workspace):
                ret.append(layer["name"].split(":")[1])
    return ret


# extract times from layer names
def get_times(layers, patten):
    times = []
    for layer in layers:
        x = re.findall(patten, layer)
        if x:
            # print(x)
            times.append(int(x[0]))
    times.sort()
    return times


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 list-geoserver-layers.py workspace layer-name-pattern small-time big-time server-url"
        )
        print(
            "Example: python3 list-geoserver-layers.py MULLER2019 paleo-age-grid-{{time}}-Ma 0 230 https://geosrv.gplates.org/geoserver/"
        )
        exit()

    _, workspace_name, name_patten, small_time, big_time, server_url = sys.argv

    # connect to geoserver
    geo = Geoserver(
        server_url,
        username=os.environ.get("username"),
        password=os.environ.get("password"),
    )

    r_name_patten = "^" + name_patten.replace("{{time}}", r"(\d+)") + "$"
    layers = get_layers(workspace_name)
    times = get_times(layers, r_name_patten)
    for time in times:
        print(name_patten.replace("{{time}}", str(time)))
    print(f"number of layers: {len(times)}")
    print("Missing times: ")
    print(list(set(range(int(small_time), int(big_time) + 1)) - set(times)))


# times = get_times(layers, r"coastlines_(\d+)Ma")
# print(len(times))
# print("Missing times: ")
# print(list(set(range(0, 231)) - set(times)))

# times = get_times(layers, r"static-polygons-(\d+)-Ma")
# print(len(times))
# print("Missing times: ")
# print(list(set(range(0, 231)) - set(times)))


# geo.delete_layer(layer_name='agri_final_proj', workspace='demo')
# geo.delete_featurestore(featurestore_name="ftry", workspace="demo")
# delete coveragestore, i.e. delete raster store
# geo.delete_coveragestore(coveragestore_name="agri_final_proj", workspace="demo")
