#!/usr/bin/env python3
import os
import csv
import time
import argparse
import multiprocessing as mp


from crawler.download_from_json import parse_json, download_repos
from crawler.get_json_from_gh import download, unzip
from verifier.uploader import read_apikey, list_all_files
from verifier.virus_total import VirusTotal

HEADER_LINE = ["Repo address", "Repo name", "Scan date", "Engine report", "Class"]
ANALYZE_TIME = 30
RETRIES = 5

def process_address(_address: str):
    _vt = vt
    fd_lock = lock

    project_name = _address.split("/")[-1] + ".zip"
    command = "wget -q -O "+project_name+ " "+_address + "/zipball/master"
    os.system(command)

    # send file
    _vt.send_files([project_name])
    time.sleep(ANALYZE_TIME)
    res_code = 0
    retry = 0
    while res_code != 200 and retry < RETRIES:
        resmap, res = _vt.retrieve_files_reports([project_name])
        res_code = res.status_code
        time.sleep(ANALYZE_TIME)
        retry += 1

    if len(resmap) > 0:
        pos = resmap["positives"]
        tot = resmap["total"]
        dat = resmap["scan_date"]

        if int(pos)/int(tot) > 0.25:
            _class = "Malicious"
        else:
            _class = "Normal"

        res_line = [_address,
                    project_name,
                    str(dat),
                    str(pos) + "/" + str(tot),
                    _class]

        fd_lock.acquire()
        _fd = open(csv_filename, "a+")
        _csv_writer = csv.writer(_fd)
        _csv_writer.writerow(res_line)
        _fd.close()
        fd_lock.release()

        if _class == "Normal":
            os.system("rm " + project_name)

        return 1
    else:
        os.system("rm " + project_name)
        return 0

def init(_l, _vt, _csv_filename):
    global lock
    global vt
    global csv_filename
    lock = _l
    vt = _vt
    csv_filename = _csv_filename

if __name__ == "__main__":


    api_key = read_apikey()
    download_path, download_name = download()
    unzip(download_path)
    address = parse_json(download_path)

    # csv preprocess
    csv_filename = "report_" + download_name +'.csv'
    csv_fd = open(csv_filename, "w+")
    csv_writer = csv.writer(csv_fd)
    csv_writer.writerow(HEADER_LINE)
    csv_fd.close()

    # dir preprocess
    _repo_path = "./repos"
    if not os.path.isdir(_repo_path):
        os.mkdir(_repo_path, 0o777)
    os.chdir(_repo_path)

    # vt init
    vt = VirusTotal(api_key=api_key,
                    is_public_api=False)

    manager = mp.Manager()
    lock = mp.Lock()
    pool = mp.Pool(initializer=init,
                   initargs=(lock, vt, csv_filename),
                   processes=mp.cpu_count()-2)

    result = pool.map(process_address, address)
