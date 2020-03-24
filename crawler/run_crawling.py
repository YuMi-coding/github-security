#!/usr/bin/env python3
"""
This file is the one-for-all process that drives all the functions of crawler
"""

from get_json_from_gh import download, unzip
from download_from_json import parse_json, download_repos, _download_from_address

if __name__ == "__main__":
    download_path, _ = download()
    unzip(download_path)
    address = parse_json(download_path)
    with open("address_list.txt", "a+") as f:
        for line in address:
            f.write(line + '\n')
    download_repos(address, download_path)