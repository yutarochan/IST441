'''
OER Commons - URL and Metadata Consolidation Script
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import json

# Application Parameters
ROOT_DIR = '../data/'

# Load Seed URL List and Metadata
seed_url = list(filter(lambda x: len(x) == 2, list(map(lambda x: x.split(','), open(ROOT_DIR + 'oer_seed_url.csv', 'r').read().split('\n')))))
metadata = json.loads(open(ROOT_DIR + 'oer_seed.json', 'rb').read())

# Convert Seed URL to Dictionary
seed_dict = {u[0] : u[1] for u in seed_url}

# Consolidate Data
for meta in metadata:
    if meta['uid'] not in seed_dict: continue
    else: meta['url'] = seed_dict[meta['uid']]

# Filter Non-Available URL Entries
metadata = list(filter(lambda x: 'url' in x, metadata))

print('PROCESSED TOTAL: ' + str(len(metadata)))

# Write New Metadata File
output = open(ROOT_DIR + 'oer_seed_master.json', 'w')
output.write(json.dumps(metadata))
output.close()

# Write URL List
output = open(ROOT_DIR + 'oer_seed_urllist.txt', 'w')
for m in metadata: output.write(m['url'] + str('\n'))
output.close()
