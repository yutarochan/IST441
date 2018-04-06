'''
HTTrack Crawler - Process Orchestrator Script
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import os
import sys
import time
import json
import subprocess as sp
from random import shuffle
import multiprocessing as mp

# Application Parameters
SEED_URL_DIR = '../../data/oer_seed_master.json'    # Seed URL Directory
HTTRACK_EXE = 'httrack'                             # HTTrack Binary Command
RAWDATA_DIR = '/Users/yutarochan/websites/'         # Location of the HTTrack Project Files

# Application Process Parameters
CPU_MAX = mp.cpu_count()    # Maximum CPU Count Obtained from System
PRC_MAX = 2                 # Hard Max of Processes to Spawn
CONN_MAX = 8                # Maximum Number of Concurrent Connections
MAX_DEPTH = 2               # Max URL Tree Depth
SHUFFLE = True              # Shuffle Order to Avoid Collision

# Build HTTrack Command
def build_command(data):
    return [HTTRACK_EXE, data['url'], '-O', "\""+RAWDATA_DIR+data['uid']+"\"", '-r'+str(MAX_DEPTH), '-c'+str(CONN_MAX), '-p1', '-D', '--quiet']

# Execute Command
def execute(command):
    print('EXECUTE: ' + ' '.join(command))
    sp.Popen(command, shell=False, stdout=sp.PIPE, stderr=sp.PIPE).wait()
    return 0

if __name__ == '__main__':
    # Import Seed URL JSON
    seed_url = json.loads(open(SEED_URL_DIR, 'r').read())[:4]

    # ~Everyday I'm Shufflin'~ to Avoid File Overwrite Collision
    if SHUFFLE: shuffle(seed_url)

    # Build HTTrack Command
    commands = list(map(build_command, seed_url))

    # Execute Command
    pool = mp.Pool(processes=PRC_MAX)
    pool.map(execute, commands)
