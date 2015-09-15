#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    openings-helper
    ~~~~~~~~~~~~~~~

    A small script for downloading videos from http://openings.moe
"""
import os
import urllib.request
import json
import sys
from argparse import ArgumentParser

# Set colors
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def controller():
    """Command line parser"""
    parser = ArgumentParser(description="Openings.moe batch downloader")
    parser.add_argument("--search", "-s", metavar="PATTERN",
            help="Search videos matching the query provided.")
    parser.add_argument("--download", "-d", metavar="PATTERN",
            help="Download all videos matching the query provided into the current working folder.")
    args = parser.parse_args()

    if args.search:
        search(args.search)
    elif args.download:
        download(args.download)
    else:
        parser.print_help()
    sys.exit()


def getvideolist():
    """Obtain all videos from the json API."""
    url = 'http://openings.moe/api/list.php'
    response = urllib.request.urlopen(url)
    lstjson = response.read().decode('utf-8', 'ignore')
    videolist = json.loads(lstjson)
    return videolist


def downloadvideo(filename):
    """Download a video with given filename."""
    url = "http://openings.moe/video/" + filename
    f = urllib.request.urlopen(url)
    print(bcolors.PURPLE + url + bcolors.ENDC + ":\nSaving to --> "
            + bcolors.YELLOW + filename + bcolors.ENDC)
    with open(os.path.basename(url), "wb") as local_file:
        local_file.write(f.read())


def download(pattern):
    """Download all videos matching the given pattern."""
    query = pattern.lower()
    videolist = getvideolist()
    for video in videolist:
        if (query in video['source'].lower()
                or query in video['file'].lower()
                or query in video['title'].lower()):
            downloadvideo(video['file'])


def search(pattern):
    """Search and return all videos matching the given pattern."""
    query = pattern.lower()
    videolist = getvideolist()
    for video in videolist:
        if (query in video['source'].lower()
                or query in video['file'].lower()
                or query in video['title'].lower()):
            print(bcolors.YELLOW + video['file'] + bcolors.ENDC + " - "
                    + video['source'] + " - " + video['title'])


if __name__ == '__main__':
    controller()
