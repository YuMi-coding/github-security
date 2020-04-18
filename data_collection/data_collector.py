# Collects entitiy data of code repositories

import csv
BENIGN_DATA = './benign.txt'
MAL_DATA = './mal_dataset.csv'

def get_repo_address():
    _res = []
    _label = []
    # this_res, this_lab = read_benign()
    # res.extend(this_res)
    # label.extend(this_lab)
    this_res, this_lab = read_mal()
    res.extend(this_res)
    label.extend(this_lab)
    return res, label

def read_benign():
    _res = []
    _label = []
    with open(BENIGN_DATA) as f:
        lines = f.readlines()
        for line in lines:
            res.append(line)
            label.append(0)
    return res, label

def read_mal():
    _res = []
    _label = []
    with open(MAL_DATA) as f:
        csv_reader = csv.reader(f)
        rows = [row for row in csv_reader]
        for i, row in enumerate(rows):
            if i == 0:
                continue
            res.append(row[0])
            string = row[1]
            prop = int(string.split('/')[0]) /int(string.split('/')[1])
            label.append(prop)
    return res, label

if __name__ == '__main__':
    res, label = get_repo_address()
    print(res)
    print(label)