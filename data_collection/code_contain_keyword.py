# Detects if the code contain keyword

import os
import shutil
from config import KEYWORDS, EXTENSION

EXTENSIONS = set(["png", "svg", "ico", "jpg", "jpg"])

def _download_from_address(_address: str, project_name: str):
    command = "wget -q -O "+project_name+ " "+_address + "/zipball/master"
    os.system(command)
    return 1

def _check_if_contains(filename: str):
    in_fd = open(filename, "r")
    try:
        lines = in_fd.readlines()
    except:
        return 0

    for line in lines:
        splitted = line.split(" ")
        for item in splitted:
            if item.lower() in KEYWORDS:
                return KEYWORDS.index(item.lower()) + 1

    return 0

def check_repo_for_keywords(_address: str):
    _repo_path = "./temp"
    if not os.path.isdir(_repo_path):
        os.mkdir(_repo_path, 0o777)
    os.chdir(_repo_path)# enter the working directory here

    project_name = _address.split("/")[-1] + ".zip"
    _download_from_address(_address, project_name)

    command = "unzip -qq -o " + project_name
    os.system(command)

    files = []
    for root, _, filename in os.walk("./"):
        for filenames in filename:
            splitted = filenames.split(".")
            if len(splitted) < 1 or splitted[-1].lower() in EXTENSION:
                files.append(os.path.join(root, filenames))

    _res = False
    for f in files:
        if _check_if_contains(f):
            _res = True
            break

    os.chdir("..")# exit the working directory here
    shutil.rmtree(_repo_path)

    return _res

if __name__ == "__main__":
    # Test scripts for this file
    TEST_ADDRESS = ["https://github.com/kcolford/blackarch",
                    "https://github.com/meedan/check-api",
                    "https://github.com/einheit/maia_mailguard_1.04a",
                    "https://github.com/secure-software-engineering/FlowDroid"]
    for address in TEST_ADDRESS:
        print("Checking", address)
        res = check_repo_for_keywords(address)
        print("Result", res)
        input()