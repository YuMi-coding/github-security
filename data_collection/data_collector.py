# Collects entitiy data of code repositories

import csv
import sys
import argparse

from user_supply_repo import get_user_from_repo, get_repo_from_user
from repo_fork_repo import get_forked_from, get_forked_to
from user_follow_user import get_user_followers, get_user_following
from code_contain_keyword import check_repo_for_keywords

EDGE_HEADER = "#source_node\tsource_class\tdest_node\tdest_class\tedge_class\n"
REPO_CLASS = "R"
USER_CLASS = "U"
REPO_HEADER = "Repo address, Repo id"
USER_HEADER = "User address, User id"

def search_dict(_dict, item):
    if item in _dict:
        return _dict[item]
    else:
        _id = len(_dict) + 1
        _dict[item] = _id
        return _id

def save_edge(edge_fd, from_id, from_class, to_id, to_class, edge_class):
    _from_id = str(from_id)
    _from_class = str(from_class)
    _to_id = str(to_id)
    _to_class = str(to_class)
    _edge_class = str(edge_class)
    line = _from_id + "\t"+\
                  _from_class + "\t" + \
                  _to_id + "\t" + \
                  _to_class + "\t" + \
                  _edge_class + "\n"
    edge_fd.write(line)
    # print(line)

def save_dict(_filename: str, _dict: dict, header: str):
    fd = open(_filename, "a")
    fd.write(header)
    writer = csv.writer(fd)
    for item in _dict:
        writer.writerow([str(item), str(_dict[item])])
    fd.close()

def process_single_address(_address: list, edge_fd, repo_dict, user_dict):
    repo_owner = get_user_from_repo(_address)
    repos_of_owner = get_repo_from_user(repo_owner)
    forked_from = get_forked_from(_address)
    forked_to = get_forked_to(_address)
    owner_follower = get_user_followers(repo_owner)
    owner_following = get_user_following(repo_owner)

    # User suppies repo, unidirectional relationship
    repo_id = search_dict(repo_dict, _address)
    repo_owner_id = search_dict(user_dict, repo_owner)
    save_edge(edge_fd, repo_id, REPO_CLASS, repo_owner_id, USER_CLASS, REPO_CLASS + "-" + USER_CLASS)

    # User supplies other repo, unidirctional relationship
    if repos_of_owner is not None:
        for single_repo_add in repos_of_owner:
            single_repo_id = search_dict(repo_dict, single_repo_add)
            save_edge(edge_fd, repo_owner_id, USER_CLASS, single_repo_id, REPO_CLASS, USER_CLASS + "-" + REPO_CLASS)

    # This repo is forked from other repos, directional relationship
    if forked_from is not None:
        forked_from_id = search_dict(repo_dict, forked_from)
        save_edge(edge_fd, forked_from_id, REPO_CLASS, repo_id, REPO_CLASS, REPO_CLASS + "->" + REPO_CLASS)

    # This repo forks into other repos
    if forked_to is not None:
        for single_forked_to in forked_to:
            single_forked_to_id = search_dict(repo_dict, single_forked_to)
            save_edge(edge_fd, repo_id, REPO_CLASS, single_forked_to_id, REPO_CLASS, REPO_CLASS + "->" + REPO_CLASS)

    # This user is followed by other users
    if owner_follower is not None:
        for follower in owner_follower:
            follower_id = search_dict(user_dict, follower)
            save_edge(edge_fd, repo_owner_id, USER_CLASS, follower_id, USER_CLASS, USER_CLASS + "->" + USER_CLASS)

    # This user followes other users
    if owner_following is not None:
        for following in owner_following:
            following_id = search_dict(user_dict, following)
            save_edge(edge_fd, following_id, USER_CLASS, repo_owner_id, USER_CLASS, USER_CLASS + "->" + USER_CLASS)

    edge_fd.flush()


def main_iteration(_filename: str, _address_list: list):
    edge_filename = _filename + "_edge.txt"
    fd = open(edge_filename, "a")
    repo_dict = {}
    user_dict = {}

    fd.write(EDGE_HEADER)
    for address in _address_list:
        process_single_address(address, fd, repo_dict, user_dict)

    fd.close()

    save_dict(output_filename + "_user.csv", user_dict, USER_HEADER)
    save_dict(output_filename + "_repo.csv", repo_dict, REPO_HEADER)

def get_address_list(_filename: str):
    input_fd = open(_filename, "r")
    reader = csv.reader(input_fd)
    _address_list = []
    for lines in reader:
        if lines[0].startswith("https:"):
            _address_list.append(lines[0])

    return _address_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get files for malicious and benign repos')
    parser.add_argument("-i", "--input", help="The input file which contains addresses of repositories", metavar="PATH")
    parser.add_argument("-o", "--output", help="Output file prefix", metavar="PATH")

    args = parser.parse_args()
    if args.input:
        input_filename = args.input
    if args.output:
        output_filename = args.output

    if not args.input or not args.output:
        print("No available input specified")
        sys.exit(1)

    address_list = get_address_list(input_filename)
    main_iteration(output_filename, address_list)
