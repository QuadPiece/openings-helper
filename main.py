# -*- coding: UTF-8 -*-

# First off, let me say: Sorry for all the ghetto code, this was my first time working with arguments in python
# I didn't follow any guide and barely touched any documentation while making this.
# As such, I have absolutely no idea what's a good way to handle arguments and I am perfectly aware that this is horrible
import os
import urllib.request
import json
import sys

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

def usage(): # Sorry in advance for this one
    print('\nUsage: main.py [option] [query]\n\n' + bcolors.YELLOW + 'Sample usage:\nmain.py --search geass\nmain.py --download geass' + bcolors.ENDC + '\n\n--search | -s\n    Searches for all videos matching the query provided.\n\n--download | -d\n    Downloads all videos matching the query provided into the current working folder.\n\nTo use multiple words in a search, surround them in quotes. eg:\nmain.py -d "Code Geass"\n')
    sys.exit()

# Obtain all videos from the json API
def getvideolist():
    url = 'http://openings.moe/api/list.php'
    response = urllib.request.urlopen(url)
    lstjson = response.read().decode('utf-8', 'ignore')
    videolist = json.loads(lstjson)
    return videolist

def checkquery():
    if len(sys.argv) <= 2:
        usage()
        sys.exit()

def downloadvideo(filename):
    url = "http://openings.moe/video/" + filename
    f = urllib.request.urlopen(url)
    print(bcolors.PURPLE + url + bcolors.ENDC + ":\nSaving to --> " + bcolors.YELLOW + filename + bcolors.ENDC)
    with open(os.path.basename(url), "wb") as local_file:
        local_file.write(f.read())

if len(sys.argv) <= 1:
    usage()
    sys.exit()

option = sys.argv[1].lower()

# Download feature
if option == "--download" or  option == "-d":
    print('\nDownloading all files matching ' + bcolors.YELLOW + sys.argv[2] + bcolors.ENDC + "\n")
    query = sys.argv[2].lower()
    videolist = getvideolist()
    for video in videolist:
        if query in video['source'].lower() or query in video['file'].lower() or query in video['title'].lower():
            downloadvideo(video['file'])
# Search feature
elif option == "--search" or option == "-s":
    print ('Searching for files matching "' + sys.argv[2] + '" from openings.moe')
    query = sys.argv[2].lower()
    videolist = getvideolist()
    for video in videolist:
        if query in video['source'].lower() or query in video['file'].lower() or query in video['title'].lower():
            print(bcolors.YELLOW + video['file'] + bcolors.ENDC + " - " + video['source'] + " - " + video['title'])
elif option == "--help" or option == "-h":
    usage()
else:
    usage()
