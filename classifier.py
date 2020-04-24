import argparse
import csv
import warnings

# from sklearn.metrics import cross_validation

from sklearn.svm import SVC, OneClassSVM
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, BaggingClassifier
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from imblearn.ensemble import BalancedBaggingClassifier

warnings.simplefilter("ignore")
DEFAULT_REPO_CSV = "./data/data_repo.csv"
DEFAULT_USER_CSV = "./data/data_user.csv"
DEFAULT_VECTOR_TXT = "./data/data2_node_vectors.txt"
DEFAULT_LIST_CSV = "./data/list.csv"

def read_repo_data(_path: str):
    repo_dict = {}
    fd = open(_path, "r")
    reader = csv.reader(fd)
    for lines in reader:
        if lines[0] == "Repo address":
            continue
        repo_dict[int(lines[1])] = lines[0]
    return repo_dict

def read_list_data(_path: str):
    truth_dict = {}
    fd = open(_path, "r")
    reader = csv.reader(fd)
    for lines in reader:
        if lines[0] == "Github repo address":
            continue
        truth_dict[lines[0]] = 1 if lines[1] == "TRUE" else 0
    return truth_dict

def assemble_ground_truth(truth_dict: dict, repo_dict: dict, vector_dict: dict):
    _X = []
    _Y = []
    _weight = []
    count_pos = 0
    count_neg = 0
    pos_weight = 0
    neg_weight = 0
    for _id in vector_dict:
        if _id in repo_dict:
            repo_add = repo_dict[_id]
            if repo_add in truth_dict:
                _class = truth_dict[repo_add]
                if _class == 0:
                    count_neg += 1
                else:
                    count_pos += 1
                _dims = vector_dict[_id]
                _X.append(_dims)
                _Y.append(_class)

    if count_pos > count_neg:
        neg_weight = count_pos/ (count_neg)
        pos_weight = 1
    else:
        pos_weight = count_neg/ (count_pos)
        neg_weight = 1

    for y in _Y:
        if y:
            _weight.append(pos_weight)
        else:
            _weight.append(neg_weight)

    return _X, _Y, _weight

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
                dims.append(float(splitted[j+1]))
            data[_id] = dims
    return data

def classifier_SVM_training(_X, _Y, _weight):
    X_train, X_test, Y_train, Y_test, w_train, w_test = train_test_split(_X, _Y, _weight, test_size=0.2, random_state=0xdeadbeef)
    clf = SVC(kernel="rbf",
              degree=5,
              gamma="auto")
    clf.fit(X_train, Y_train, w_train)
    # print(X_train)
    # print(sum(Y_train))
    y_pred = clf.predict(X_test)
    # print(sum(y_pred))
    print("Result from labeled SVM:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_test, y_pred).ravel())

def classifier_imblearn_SVM_training(_X, _Y, _weight):
    X_train, X_test, Y_train, Y_test, w_train, w_test = train_test_split(_X, _Y, _weight, test_size=0.2, random_state=0xdeadbeef)
    bbc = BalancedBaggingClassifier(base_estimator=SVC(kernel="rbf",
                                                       gamma="auto"),
                                    n_estimators=10,
                                    sampling_strategy="auto",
                                    max_samples=80,
                                    replacement=False,
                                    random_state=0xdeadbeef)
    bbc.fit(X_train, Y_train)
    y_pred = bbc.predict(X_test)
    print("Result from bagging labeled SVM:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_test, y_pred).ravel())

def classifier_oneSVM_training(_X, _Y, _weight):
    # clf = SVC()
    # clf.fit(_X, _Y, _weight)
    # y_pred = clf.predict(_X)
    # print(accuracy_score(_Y, y_pred))
    # print(confusion_matrix(_Y, y_pred).ravel())
    X_train, X_test, Y_train, Y_test = train_test_split(_X, _Y, test_size=0.2, random_state=0xdeadbeef)
    train_normal = []
    train_outliner = []
    for i, attributes in enumerate(X_train):
        if Y_train[i] == 0:
            train_normal.append(attributes)
        else:
            train_outliner.append(attributes)
    outliner_prop = len(train_outliner) / len(train_normal)
    clf = OneClassSVM(kernel="rbf", \
                      nu=outliner_prop,\
                      degree=5,\
                      gamma="auto")
    clf.fit(train_normal)
    y_pred = clf.predict(X_test)
    Y_pred = []
    for y in y_pred:
        if y == 1:
            Y_pred.append(0)
        else:
            Y_pred.append(1)
    print("Result from OneClass SVM:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_test, Y_pred).ravel())

def classifier_isoforest_training(_X, _Y, _weight):
    X_train, X_test, Y_train, Y_test = train_test_split(_X, _Y, test_size=0.2, random_state=0xdeadbeef)
    train_normal = []
    train_outliner = []
    for i, attributes in enumerate(X_train):
        if Y_train[i] == 0:
            train_normal.append(attributes)
        else:
            train_outliner.append(attributes)
    # outliner_prop = len(train_outliner) / len(train_normal)
    clf = IsolationForest(random_state=0)
    clf.fit(train_normal)
    y_pred = clf.predict(X_test)
    Y_pred = []
    for y in y_pred:
        if y == 1:
            Y_pred.append(0)
        else:
            Y_pred.append(1)
    print("Result from Isolation Forest:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_test, Y_pred).ravel())

def classifier_outliner_training(_X, _Y, _weight):
    X_train, X_test, Y_train, Y_test = train_test_split(_X, _Y, test_size=0.8, random_state=0xdeadbeef)
    train_normal = []
    train_outliner = []
    for i, attributes in enumerate(X_train):
        if Y_train[i] == 0:
            train_normal.append(attributes)
        else:
            train_outliner.append(attributes)
    # outliner_prop = len(train_outliner) / len(train_normal)
    clf = LocalOutlierFactor(n_neighbors=2)
    y_pred = clf.fit_predict(X_train)
    Y_pred = []
    for y in y_pred:
        if y == 1:
            Y_pred.append(0)
        else:
            Y_pred.append(1)
    print("Result from Outliner Factor:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_train, Y_pred).ravel())

def classifier_elliptic_training(_X, _Y, _weight):
    X_train, X_test, Y_train, Y_test = train_test_split(_X, _Y, test_size=0.2, random_state=0xdeadbeef)
    train_normal = []
    train_outliner = []
    for i, attributes in enumerate(X_train):
        if Y_train[i] == 0:
            train_normal.append(attributes)
        else:
            train_outliner.append(attributes)
    # outliner_prop = len(train_outliner) / len(train_normal)
    clf = EllipticEnvelope(random_state=0).fit(train_normal)
    clf.fit(train_normal)
    y_pred = clf.predict(X_test)
    Y_pred = []
    for y in y_pred:
        if y == 1:
            Y_pred.append(0)
        else:
            Y_pred.append(1)
    print("Result from Elliptic Envelope:")
    print("tn, fp, fn, tp =", confusion_matrix(Y_test, Y_pred).ravel())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The classifier that works on random walk vectors")
    parser.add_argument("-r", "--repo", help="The repository mapping file", metavar="PATH")
    parser.add_argument("-u", "--user", help="The user mapping file", metavar="PATH")
    parser.add_argument("-v", "--vectors", help="The vectors of node", metavar="PATH")
    parser.add_argument("-l", "--list", help="The ground truth list file", metavar="PATH")
    args = parser.parse_args()

    repo_csv_path = args.repo if args.repo else DEFAULT_REPO_CSV
    user_csv_path = args.user if args.user else DEFAULT_USER_CSV
    vector_path = args.vectors if args.vectors else DEFAULT_VECTOR_TXT
    list_path = args.list if args.list else DEFAULT_LIST_CSV

    repo_data = read_repo_data(repo_csv_path)
    truth_data = read_list_data(list_path)
    vector_data = read_vector_data(vector_path)

    X, Y, weight = assemble_ground_truth(truth_data, repo_data, vector_data)
    classifier_SVM_training(X, Y, weight)
    classifier_oneSVM_training(X, Y, weight)
    classifier_isoforest_training(X, Y, weight)
    classifier_elliptic_training(X, Y, weight)
    classifier_outliner_training(X, Y, weight)
    classifier_imblearn_SVM_training(X, Y, weight)