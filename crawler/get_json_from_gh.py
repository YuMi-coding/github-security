#!/usr/bin/env python3
"""
This code downloads json file from github archive:
https://www.gharchive.org/
Which gives publicaly available github modification
at a hour granularity
"""
import os

def download():
    current_path = os.path.dirname(os.path.abspath(__file__))
    _download_path = current_path + "/download_res"

    if not os.path.isdir(_download_path):
        os.mkdir(_download_path, 0o777)
    os.chdir(_download_path)

    _download_file = input("The time of archives to download(YYYY-MM-{DD}-{HH}): ")
    command = "wget -q https://data.gharchive.org/" + _download_file + ".json.gz"
    os.system(command)
    print("Download complete!")
    return _download_path

def unzip(_download_path):
    _filenames = [f for f in os.listdir(_download_path) \
        if os.path.isfile(os.path.join(_download_path, f))]

    _unzip_list = []
    for name in _filenames:
        if name.endswith(".json.gz"):
            _unzip_list.append(name)

    for name in _unzip_list:
        print("unzipping:", name)
        command = "gunzip "+ name
        os.system(command)


if __name__ == "__main__":
    download_path = download()

    unzip(download_path)