#!/usr/bin/env python
# zip the shapefiles.
# The "-j" option is very important.
# It will not create folders inside the zip file. It is important for geoserver.

import os
import sys
from pathlib import Path

script_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 zip-shapefiles.py input-folder output-folder")
        exit()

    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"{data_dir} does not exist!")
        exit(1)
    output_dir = sys.argv[2]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for path in Path(data_dir).rglob("*.shp"):
        print(path.stem)
        zip_fn = f"{output_dir}/{path.stem}.zip"
        os.system(f"zip -j {zip_fn} {data_dir}/{path.stem}.*")
