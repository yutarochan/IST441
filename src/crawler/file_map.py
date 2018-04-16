'''
File Mapper: Crawl Indexer
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import os

def walkdir(dirname):
    for cur, _dirs, files in os.walk(dirname):
        pref = ''
        head, tail = os.path.split(cur)
        while head:
            pref += '---'
            head, _tail = os.path.split(head)
        print(pref+tail)
        for f in files:
            print(pref+'---'+f)

if __name__ == '__main__':
    # List Files in OER Project Dump
    # Build Tree Data Structure
