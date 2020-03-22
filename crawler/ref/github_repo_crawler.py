"""
Code to download git repos according to a file and zip them up
"""

import os
import copy
ADDRESS_FILE_PATH = "./git_backdoor_repos.txt"
def main():
    _file_desc = open(ADDRESS_FILE_PATH, "r")
    file_lines = _file_desc.readlines()
    current_path = os.path.dirname(os.path.abspath(__file__))
    download_path = current_path + "/download_res"
    if not os.path.isdir(download_path):
        os.mkdir(download_path, 0o777)
    os.chdir(download_path)
    for _address in file_lines:
        print("Downloading from:", _address)
        project_name = copy.deepcopy(_address)
        project_name = project_name.split("/")[-1][:-1]
        command = "wget -O "+ project_name +" "+ _address[:-1] + "/zipball/master"
        print(command)
        os.system(command)
        # input()
        print("Download complete")


if __name__ == '__main__':
    main()