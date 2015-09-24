#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    openings-helper
    ~~~~~~~~~~~~~~~
    A small download script for http://openings.moe
"""

import os
import sys
import json
from argparse import ArgumentParser
try:
    import urllib.request as urlreq
except ImportError:  # Python 2 support.
    import urllib2 as urlreq


# Set colors
class Colors:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def safeprint(text):
    """Safely print text with unicode"""
    while True:
        try:
            print(text)
            break
        except UnicodeEncodeError as ex:
            text = (text[0:ex.start] + "(unicode)" + text[ex.end:])


def getfile(url):
    """Get file over HTTP"""
    try:
        return urlreq.urlopen(url)
    except urlreq.HTTPError as e:
        safeprint("Sever returned with response code " + str(e.getcode()) + ", download failed.")


def getvideolist():
    """Fetch list of all videos from the JSON API."""
    safeprint("Getting video list...")
    response = getfile("http://openings.moe/api/list.php")
    lstjson = response.read().decode("utf-8", "ignore")
    videolist = json.loads(lstjson)
    return videolist


def downloadvideo(filename):
    """Download a video based on given filename."""
    url = "http://openings.moe/video/" + filename
    f = getfile(url)
    safeprint(Colors.PURPLE + url + Colors.END + ":\nSaving to --> " + Colors.YELLOW + filename + Colors.END)
    with open(os.path.basename(url), "wb") as local_file:
        try:
            local_file.write(f.read())
        except IOError as e:
            safeprint("An error occurred while saving the file, try again. " + str(e))


def download(pattern):
    """Download all videos matching the given pattern."""
    query = pattern.lower()
    videolist = getvideolist()
    filename = []
    for video in videolist:
        for value in video.values():
            if query in str(value).lower():
                filename.append(video["file"])
    if filename:
        for name in filename:
            downloadvideo(name)
    else:
        safeprint("No video matching the given query was found.")


def search(pattern):
    """Search and return all videos matching the given pattern."""
    query = pattern.lower()
    videolist = getvideolist()
    results = []
    for video in videolist:
        for value in video.values():
            if query in str(value).lower():
                results.append(Colors.YELLOW + video["file"] + Colors.END + " - " + video["source"] + " - " +
                               video["title"])
    if results:
        for result in results:
            safeprint(result)
    else:
        safeprint("No video matching the given query was found.")


def main():
    """Command line parser"""
    parser = ArgumentParser(description="Openings.moe batch downloader")
    parser.add_argument("--search", "-s", metavar="PATTERN", help="Search videos matching the query provided.")
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


if __name__ == "__main__":
    main()
