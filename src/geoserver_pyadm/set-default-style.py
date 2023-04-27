#!/usr/bin/env python
import os
import sys
import time

from dotenv import load_dotenv
from geo.Geoserver import Geoserver

workspace_name = "MULLER2019"
server_url = "https://geosrv.earthbyte.org/geoserver/"

script_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(f"{script_path}/.env")  # take environment variables from .env.

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(
            "Usage: python3 set-default-style.py workspace layer-name-pattern style-name small-time big-time server-url"
        )
        print(
            "Example: python3 set-default-style.py MULLER2019 static-polygons-{{time}}-Ma polygon-no-fill 0 230 https://geosrv.gplates.org/geoserver/"
        )
        exit()

    (
        _,
        workspace_name,
        name_patten,
        style_name,
        small_time,
        big_time,
        server_url,
    ) = sys.argv

    # connect to geoserver
    geo = Geoserver(
        server_url,
        username=os.environ.get("username"),
        password=os.environ.get("password"),
    )
    for age in range(int(small_time), int(big_time) + 1):
        print(age)
        geo.publish_style(
            layer_name=name_patten.replace("{{time}}", str(age)),
            style_name="polygon-no-fill",
            workspace=workspace_name,
        )
        time.sleep(3)
