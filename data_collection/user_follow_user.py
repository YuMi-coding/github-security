# Detects the user who may follow other users
import os

GITHUB_HEADER = 'https://github.com'

def get_user_followers(_address: str):
    _temp_path = "./temp"
    if not os.path.isdir(_temp_path):
        os.mkdir(_temp_path, 0o777)
    os.chdir(_temp_path)# enter the working directory here

    if _address.endswith("/"):
        temp_address = _address[:-1]
    user_name = temp_address.split("/")[-1]
    if user_name.endswith("\n"):
        user_name.replace("\n", "")

    html_name = _address.split("/")[-1] + "_user_follower.html"
    command = "wget -q -O " + html_name + " " + _address + "?tab=followers"
    os.system(command)

    res = set()
    fd = open(html_name, "r")
    lines = fd.readlines()
    for line in lines:
        if "href=" in line and "/users/" in line:
            href_split = line.split("href=")[1]
            comment_split = href_split.split("\"")[1]
            splash_split = comment_split.split("/")
            # print(comment_split)
            if len(splash_split) == 2 and "?" not in comment_split: # only length of 3 means a repo address
                # print(comment_split)
                res.add(GITHUB_HEADER + comment_split)

    command = "rm " + html_name
    os.system(command)
    os.chdir("..") # exit the directory
    res = list(res)
    if len(res) == 0: # Nothing in followers list
        res = None

    return res

def get_user_following(_address: str):
    _temp_path = "./temp"
    if not os.path.isdir(_temp_path):
        os.mkdir(_temp_path, 0o777)
    os.chdir(_temp_path)# enter the working directory here

    if _address.endswith("/"):
        temp_address = _address[:-1]
    user_name = temp_address.split("/")[-1]
    if user_name.endswith("\n"):
        user_name.replace("\n", "")

    html_name = _address.split("/")[-1] + "_user_following.html"
    command = "wget -q -O " + html_name + " " + _address + "?tab=following"
    os.system(command)

    res = set()
    fd = open(html_name, "r")
    lines = fd.readlines()
    for line in lines:
        if "href=" in line and "/users/" in line:
            href_split = line.split("href=")[1]
            comment_split = href_split.split("\"")[1]
            splash_split = comment_split.split("/")
            # print(comment_split)
            if len(splash_split) == 2 and "?" not in comment_split: # only length of 3 means a repo address
                # print(comment_split)
                res.add(GITHUB_HEADER + comment_split)

    command = "rm " + html_name
    os.system(command)
    os.chdir("..") # exit the directory
    res = list(res)
    if len(res) == 0: # Nothing in followers list
        res = None

    return res

if __name__ == "__main__":
    # Test script for this file

    TEST_USER = ["https://github.com/0064Unknown/",
                 "https://github.com/00NoisyMime00/",
                 "https://github.com/0420syj/",
                 "https://github.com/05nelsonm/"]

    for address in TEST_USER:
        print(get_user_followers(address))
    input("user followers complete")

    for address in TEST_USER:
        print(get_user_following(address))
    input("user following complete")