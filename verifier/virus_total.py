"""
The library for Virus Total operations
Reference code from:
https://github.com/subbyte/virustotal
"""
import os
import time
import logging
import json
import hashlib
import requests


def sha256sum(filename):
    """
    Efficient sha256 checksum realization
    Take in 8192 bytes each time
    The block size of sha256 is 512 bytes
    """
    with open(filename, 'rb') as f:
        m = hashlib.sha256()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

class VirusTotal():
    def __init__(self, api_key="", is_public_api=True):
        self.apikey = api_key
        self.URL_BASE = "https://www.virustotal.com/vtapi/v2/"
        self.HTTP_OK = 200

        # whether the API_KEY is a public API. limited to 4 per min if so.
        self.is_public_api = is_public_api
        # whether a retrieval request is sent recently
        self.has_sent_retrieve_req = False
        # if needed (public API), sleep this amount of time between requests
        self.PUBLIC_API_SLEEP_TIME = 20

        self.logger = logging.getLogger("virt-log")
        self.logger.setLevel(logging.INFO)
        self.scrlog = logging.StreamHandler()
        self.scrlog.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(self.scrlog)
        self.is_verboselog = False

    def send_files(self, filenames):
        """
        Send files to scan
        @param filenames: list of target files
        """
        url = self.URL_BASE + "file/scan"
        attr = {"apikey": self.apikey}

        for filename in filenames:
            files = {"file": open(filename, 'rb')}
            try:
                res = requests.post(url, data=attr, files=files)

                if res.status_code == self.HTTP_OK:
                    resmap = json.loads(res.text)
                    if not self.is_verboselog:
                        self.logger.info("sent: %s, HTTP: %d, response_code: %d, scan_id: %s",
                                         os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_id"])
                    else:
                        self.logger.info("sent: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
                else:
                    self.logger.warning("sent: %s, HTTP: %d", os.path.basename(filename), res.status_code)
            except Exception as e:
                print(e)

    def retrieve_files_reports(self, filenames):
        """
        Retrieve Report for file
        @param filename: target file
        """
        resmap = {}
        for filename in filenames:
            res = self.retrieve_report(sha256sum(filename))

            if res.status_code == self.HTTP_OK:
                try:
                    resmap = json.loads(res.text)
                    if not self.is_verboselog and "scan_date" in resmap:
                        self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
                                         os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
                    else:
                        self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
                except Exception as e:
                    print(e)
            else:
                self.logger.warning("retrieve report: %s, HTTP: %d", os.path.basename(filename), res.status_code)
        return resmap, res
    def retrieve_from_meta(self, filename):
        """
        Retrieve Report for checksums in the metafile
        @param filename: metafile, each line is a checksum, best use sha256
        """
        with open(filename) as f:
            for line in f:
                checksum = line.strip()
                res = self.retrieve_report(checksum)

                if res.status_code == self.HTTP_OK:
                    resmap = json.loads(res.text)
                    if not self.is_verboselog:
                        self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
                                         checksum, res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
                    else:
                        self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
                else:
                    self.logger.warning("retrieve report: %s, HTTP: %d", checksum, res.status_code)

    def retrieve_report(self, chksum):
        """
        Retrieve Report for the file checksum
        4 retrieval per min if only public API used
        @param chksum: sha256sum of the target file
        """
        if self.has_sent_retrieve_req and self.is_public_api:
            time.sleep(self.PUBLIC_API_SLEEP_TIME)

        url = self.URL_BASE + "file/report"
        params = {"apikey": self.apikey, "resource": chksum}
        res = requests.post(url, data=params)
        self.has_sent_retrieve_req = True
        return res