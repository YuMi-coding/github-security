#!/usr/bin/env python3
"""
This is script to parse the logfile from uploader
"""

import argparse

PREC_PATTERN_STRING = "positives/total:"
NAME_PATTERN_STRING = "retrieve report:"
LOWERBOUND = 5
def parse_log(_filename):
    fd = open(_filename, "r")
    fd_lines = fd.readlines()

    for lines in fd_lines:
        if PREC_PATTERN_STRING in lines:
            _ind = lines.index(PREC_PATTERN_STRING)
            perc_string = lines[_ind + len(PREC_PATTERN_STRING):]
            pos = int(perc_string.split("/")[0])
            tot = int(perc_string.split("/")[1])

            _ind = lines.index(NAME_PATTERN_STRING)
            name_string = lines[_ind + len(NAME_PATTERN_STRING):]
            _name = name_string.split(",")[0]
            if pos > LOWERBOUND:
                print(_name, "  ", pos, "/", tot)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse the logfile to find malicious samples')
    parser.add_argument("-i", "--input", help="the logfile to parse", metavar="FILE")

    args = parser.parse_args()

    filename = args.input
    parse_log(filename)
