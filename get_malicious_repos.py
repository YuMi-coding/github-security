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
ANALYZE_TIME = 300
RETRIES = 5
COMPLETE_RESPONSE_CODE = 1
PROCESSES = 300

def process_address(_address: str):
    _vt = vt
    # fd_lock = lock

    project_name = _address.split("/")[-1] + ".zip"
    command = "wget -q -O "+project_name+ " "+_address + "/zipball/master"
    os.system(command)

    # send file
    try:
        _vt.send_files([project_name])
    except Exception as e:
        print(e)
    res_code = 0
    retry = 0
    while res_code != COMPLETE_RESPONSE_CODE and retry < RETRIES:
        time.sleep(ANALYZE_TIME)
        try:
            resmap, res = _vt.retrieve_files_reports([project_name])
        except Exception as e:
            print(e)
            return 0
        res_code = res.status_code
        if "scan_date" in resmap and 'positives' in resmap and 'total' in resmap:
            continue_flag = False
            if continue_flag:
                continue
            else:
                break
        retry += 1

    if res_code == 200:
        _class = "Normal"
        try:
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

            lock.acquire()
            # print("lock acquired")
            _fd = open(csv_filename, "a+")
            _csv_writer = csv.writer(_fd)
            _csv_writer.writerow(res_line)
            _fd.close()
            lock.release()
            # print("lock released")
        except Exception as e:
            print(e)

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
    csv_filename = "../" + csv_filename

    # dir preprocess
    _repo_path = "./repos_mal"
    if not os.path.isdir(_repo_path):
        os.mkdir(_repo_path, 0o777)
    os.chdir(_repo_path)

    # vt init
    vt = VirusTotal(api_key=api_key,
                    is_public_api=False)

    manager = mp.Manager()
    lock = mp.Lock()
    # lock.release()
    pool = mp.Pool(initializer=init,
                   initargs=(lock, vt, csv_filename),
                   processes=PROCESSES)

    result = pool.map(process_address, address)
