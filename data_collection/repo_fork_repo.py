# Detects the repo that forks from each other
import os

GITHUB_HEADER = 'https://github.com'

def get_forked_from(_address: str):
    _temp_path = "./temp"
    if not os.path.isdir(_temp_path):
        os.mkdir(_temp_path, 0o777)
    os.chdir(_temp_path)# enter the working directory here

    project_name = _address.split("/")[-1] + ".html"
    command = "wget -q -O " + project_name + " " + _address
    os.system(command)

    res = None
    fd = open(project_name, "r")
    lines = fd.readlines()
    for line in lines:
        if "forked from" in line:
            last_addr = line.split("href=")[-1]
            forked_from_addr = last_addr.split("\"")[1]
            if forked_from_addr is not None:
                res = forked_from_addr
                break

    command = "rm " + project_name
    os.system(command)
    os.chdir("..") # exit the directory
    return res

def get_forked_to(_address: str):
    _temp_path = "./temp"
    if not os.path.isdir(_temp_path):
        os.mkdir(_temp_path, 0o777)
    os.chdir(_temp_path)# enter the working directory here

    project_name = _address.split("/")[-1]
    if project_name.endswith("\n"):
        project_name.replace("\n", "")
    html_name = _address.split("/")[-1] + "_network.html"
    command = "wget -q -O " + html_name + " " + _address + "/network/members"
    os.system(command)

    res = set()
    fd = open(html_name, "r")
    lines = fd.readlines()
    for line in lines:
        if "href=" in line and project_name in line:
            href_split = line.split("href=")[1]
            comment_split = href_split.split("\"")[1]
            splash_split = comment_split.split("/")
            if len(splash_split) == 3: # only length of 3 means a repo address
                res.add(GITHUB_HEADER + comment_split)

    command = "rm " + html_name
    os.system(command)
    os.chdir("..") # exit the directory
    res = list(res)
    if len(res) == 1: # the repo only has itself in network
        res = None

    return res

if __name__ == "__main__":
    # Test script for this file
    TEST_ADDRESS = ["https://github.com/0064Unknown/lede",
                    "https://github.com/00NoisyMime00/Tick-Tac-Toe",
                    "https://github.com/1725636955/eladmin",
                    "https://github.com/05nelsonm/authentication-manager"]
    for address in TEST_ADDRESS:
        print(get_forked_from(address))

    input("finished forked from")

    for address in TEST_ADDRESS:
        print(get_forked_to(address))
        input()
    input("finished forked to")
