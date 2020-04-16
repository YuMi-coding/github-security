#!/usr/bin/env python3
import os
import sys
import argparse
import logging

from virus_total import VirusTotal


def list_all_files(path):
    """
    List all file paths
    @param path: if it is a path, just return, if dir, return paths of files in it
    Subdirectories not listed
    No recursive search
    """
    assert os.path.isfile(path) or os.path.isdir(path)

    if os.path.isfile(path):
        return [path]
    else:
        return filter(os.path.isfile, map(lambda x: '/'.join([os.path.abspath(path), x]), os.listdir(path)))

def read_apikey():
    current_path = os.path.dirname(os.path.abspath(__file__))
    api_key_path = os.path.join(current_path, "api.key")
    if os.path.isfile(api_key_path):
        fd = open(api_key_path, "r")
        lines = fd.readlines()
        _api_key = lines[0]
    else:
        _api_key = input("paste your API key here:")

    return _api_key

if __name__ == "__main__":
    api_key = read_apikey()
    vt = VirusTotal(api_key)

    parser = argparse.ArgumentParser(description='Virustotal File Scan')
    parser.add_argument("-p", "--private", help="the API key belongs to a private API service", action="store_true")
    parser.add_argument("-v", "--verbose", help="print verbose log (everything in response)", action="store_true")
    parser.add_argument("-s", "--send", help="send a file or a directory of files to scan", metavar="PATH")
    parser.add_argument("-r", "--retrieve", help="retrieve reports on a file or a directory of files", metavar="PATH")
    parser.add_argument("-m", "--retrievefrommeta", help="retrieve reports based on checksums in a metafile (one sha256 checksum for each line)", metavar="METAFILE")
    parser.add_argument("-l", "--log", help="log actions and responses in file", metavar="LOGFILE")
    args = parser.parse_args()

    if args.log:
        filelog = logging.FileHandler(args.log)
        filelog.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S"))
        vt.logger.addHandler(filelog)

    if args.private:
        vt.is_public_api = False

    if args.verbose:
        vt.is_verboselog = True

    # system init end, start to perform operations
    api_comments = {True: 'Public', False: 'Private'}
    vt.logger.info("API KEY loaded. %s API used.", api_comments[vt.is_public_api])

    start = 0
    end = 400

    if args.send:
        file_list = list(list_all_files(args.send))
        vt.send_files(file_list)

    if args.retrieve:
        file_list = list(list_all_files(args.retrieve))
        vt.retrieve_files_reports(file_list)

    if args.retrievefrommeta:
        file_list = list(list_all_files(args.retrievefrommeta))
        vt.retrieve_from_meta(file_list)