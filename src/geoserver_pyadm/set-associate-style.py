#!/usr/bin/env python
import os
import sys

import requests
from dotenv import load_dotenv
from geo.Geoserver import Geoserver

workspace_name = "MULLER2019"
server_url = "https://geosrv.earthbyte.org/geoserver/"

script_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(f"{script_path}/.env")  # take environment variables from .env.


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(
            "Usage: python3 set-associate-style.py workspace layer-name-pattern style-name small-time big-time server-url"
        )
        print(
            "Example: python3 set-associate-style.py MULLER2019 static-polygons-{{time}}-Ma polygon-no-fill 0 230 https://geosrv.gplates.org/geoserver/"
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

    username = os.environ.get("username")
    passwd = os.environ.get("password")

    # connect to geoserver
    geo = Geoserver(
        server_url,
        username=username,
        password=passwd,
    )

    for age in range(int(small_time), int(big_time) + 1):
        layer_name = name_patten.replace("{{time}}", str(age))
        url = (
            f"https://{username}:{passwd}"
            + f"@{server_url[8:]}/rest/layers/{workspace_name}:{layer_name}/styles"
        )
        ret = requests.get(url)

        if style_name not in ret.text:
            print(age)
            # add the style to associated style list
            url = f"https://{username}:{passwd}@{server_url[8:]}/rest/layers/{workspace_name}:{layer_name}"
            headers = {"content-type": "text/xml"}
            requests.put(
                url,
                data=f"<layer><styles><style><name>{workspace_name}:{style_name}</name></style></styles></layer>",
                headers=headers,
            )
