# Detects the user that supplies this repo

import os

GITHUB_HEADER = 'https://github.com'

def get_user_from_repo(_address: str):
    repo_name = _address.split("/")[-1]
    user = _address.replace(repo_name, "")
    return user

def get_repo_from_user(_address: str):
    _temp_path = "./temp"
    if not os.path.isdir(_temp_path):
        os.mkdir(_temp_path, 0o777)
    os.chdir(_temp_path)# enter the working directory here

    if _address.endswith("/"):
        temp_address = _address[:-1]
    user_name = temp_address.split("/")[-1]
    if user_name.endswith("\n"):
        user_name.replace("\n", "")

    # print(user_name)

    html_name = _address.split("/")[-1] + "_user.html"
    command = "wget -q -O " + html_name + " " + _address
    os.system(command)

    res = set()
    fd = open(html_name, "r")
    lines = fd.readlines()
    for line in lines:
        if "href=" in line and user_name in line:
            href_split = line.split("href=")[1]
            comment_split = href_split.split("\"")[1]
            splash_split = comment_split.split("/")
            if len(splash_split) == 3 and splash_split[1] == user_name: # only length of 3 means a repo address
                # print(comment_split)
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
                    "https://github.com/0420syj/kosm",
                    "https://github.com/05nelsonm/authentication-manager"]
    for address in TEST_ADDRESS:
        print(get_user_from_repo(address))
    input("user from repo complete")

    TEST_USER = ["https://github.com/0064Unknown/",
                 "https://github.com/00NoisyMime00/",
                 "https://github.com/0420syj/",
                 "https://github.com/05nelsonm/"]

    for address in TEST_USER:
        print(get_repo_from_user(address))
    input("repo from user complete")