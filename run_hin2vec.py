import os

if __name__ == "__main__":
    os.chdir("./hin2vec-master/")
    command = "python main.py ../data/data_edge.txt ../data/data2_node_vectors.txt ../data/data2_metapath_vectors.txt -l 1000 -d 10 -w 5"
    os.system(command)
    os.chdir("..")