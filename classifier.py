import argparse
import csv

DEFAULT_REPO_CSV = "./data/data_repo.csv"
DEFAULT_USER_CSV = "./data/data_user.csv"
DEFAULT_VECTOR_TXT = "./data/data_node_vectors.txt"
DEFAULT_LIST_CSV = "./data/list.csv"

def read_repo_data(_path: str):
    repo_dict = {}
    fd = open(_path, "r")
    reader = csv.reader(fd)
    for lines in reader:
        repo_dict[lines[1]] = int(lines[0])
    return repo_dict

def read_list_data(_path: str):
    truth_dict = {}
    fd = open(_path, "r")
    reader = csv.reader(fd)
    for lines in reader:
        truth_dict[lines[0]] = 1 if lines[1] == "TRUE" else 0
    return truth_dict

def read_vector_data(_path: str):
    fd = open(_path, "r")
    _count = 0
    _dim = 0
    lines = fd.readlines()
    data = {}
    for i, line in enumerate(lines):
        if i == 0:
            splitted = line.split(" ")
            _count = int(splitted[0])
            _dim = int(splitted[1])
        else:
            splitted = line.split(" ")
            _id = int(splitted[0])
            dims = []
            for j in range(_dim):
                dims.append(int(splitted[j+1]))
            data[_id] = dims
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The classifier that works on random walk vectors")
    parser.add_argument("-r", "--repo", help="The repository mapping file", metavar="PATH")
    parser.add_argument("-u", "--user", help="The user mapping file", metavar="PATH")
    parser.add_argument("-v", "--vectors", help="The vectors of node", metavar="PATH")
    parser.add_argument("-l", "--list",help="The ground truth list file", metavar="PATH")
    args = parser.parse_args()

    repo_csv_path = args.repo if args.repo else DEFAULT_REPO_CSV
    user_csv_path = args.user if args.user else DEFAULT_USER_CSV
    vector_path = args.vectors if args.vectors else DEFAULT_VECTOR_TXT
    list_path = args.list if args.list else DEFAULT_LIST_CSV

    repo_data = read_repo_data(repo_csv_path)
    truth_data = read_list_data(list_path)
    