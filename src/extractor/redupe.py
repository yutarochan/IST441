'''
Duplication Reduction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import json

# Load Raw Text Metadata
meta = list(filter(None, json.loads(open('oer_metadata.json', 'r').read())))

# Build Direct UUID Map
uuid_map = dict()
for m in meta: uuid_map[m['uuid']] = m

# Build URL Treemap
url_map = dict()
for uuid in uuid_map:
    if 'url' not in uuid_map[uuid]: continue
    if uuid_map[uuid]['url'] not in url_map: 
        url_map[uuid_map[uuid]['url']] = []
    url_map[uuid_map[uuid]['url']].append(uuid)

print(len(uuid_map.keys()))

# Filter Duplicates
for url in url_map:
    if len(url_map[url]) > 1:
        for uuid in url_map[url][1:]: del uuid_map[uuid]

print(len(uuid_map.keys()))

