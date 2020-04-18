#!/usr/bin/env python3
"""
This code parses json file from gharchive and generates
list of address that we can download from
"""
import os
import multiprocessing as mp

def parse_json(_download_path):
    _filenames = [f for f in os.listdir(_download_path) \
        if os.path.isfile(os.path.join(_download_path, f))]
    os.chdir(_download_path)

    _json_list = []
    for name in _filenames:
        if name.endswith(".json"):
            _json_list.append(name)

    _res_set = set()
    for _json_name in _json_list:
        _fd = open(_json_name, 'r')
        _fd_lines = _fd.readlines()
        for lines in _fd_lines:
            if "html_url" in lines:
                index_start = lines.index("html_url") + 11
                i = index_start
                while lines[i] != "\"":
                    i += 1
                this_url = lines[index_start: i]
                if len(this_url.split("/")) >= 5: # Valid repo address
                    url_all = this_url.split("/")[:5]
                    _url = "/".join(url_all)
                    _res_set.add(_url)
                    print(_url)

    return list(_res_set)

def _download_from_address(_address: str):
    project_name = _address.split("/")[-1] + ".zip"
    command = "wget -q -O "+project_name+ " "+_address + "/zipball/master"
    os.system(command)
    print("Download ", project_name, " complete!")
    return 1

def download_repos(_address_list, _download_path):
    _repo_path = "./repos"
    if not os.path.isdir(_repo_path):
        os.mkdir(_repo_path, 0o777)
    os.chdir(_repo_path)

    process_pool = mp.Pool(processes=mp.cpu_count()-2)


    output = process_pool.map(_download_from_address, _address_list)
    print("Downloaded", sum(output), "repos")

if __name__ == "__main__":
    download_path = "./download_res"
    address = parse_json(download_path)
    with open("address_list.txt", "a+") as f:
        for line in address:
            f.write(line + '\n')
    download_repos(address, download_path)