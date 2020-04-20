import csv
import random

MAX_BENIGN_REPOS = 900
BENIGN_DATA = './benign.txt'
MAL_DATA = './mal_dataset.csv'

CSV_HEADER = "Github repo address, Malicious or not\n"
def get_repo_address():
    _res = []
    _label = []

    this_res, this_lab = read_benign()

    count_benign = 0
    for i, item in enumerate(this_res):
        if count_benign > MAX_BENIGN_REPOS:
            break
        if random.random() > 0.8:
            _res.append(item)
            _label.append(this_lab[i])
            count_benign += 1

    this_res, this_lab = read_mal()
    _res.extend(this_res)
    _label.extend(this_lab)
    return _res, _label

def read_benign():
    _res = []
    _label = []
    with open(BENIGN_DATA) as f:
        lines = f.readlines()
        for line in lines:
            _res.append(line)
            _label.append(False)
    return _res, _label

def read_mal():
    _res = []
    _label = []
    with open(MAL_DATA) as f:
        csv_reader = csv.reader(f)
        rows = [row for row in csv_reader]
        for i, row in enumerate(rows):
            if i == 0:
                continue
            _res.append(row[0])
            string = row[1]
            prop = int(string.split('/')[0]) /int(string.split('/')[1])
            _label.append(prop > 0)
    return _res, _label

def write_csv(res, label):
    fd = open("list.csv", "w")
    fd.write(CSV_HEADER)
    writer = csv.writer(fd)

    for i, _ in enumerate(res):
        _res = res[i].replace("\n", "")
        writer.writerow([_res, label[i]])

if __name__ == "__main__":
    _res, _lab = get_repo_address()
    write_csv(_res, _lab)