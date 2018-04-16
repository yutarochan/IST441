'''
File Directory - Deduplication Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
from functools import reduce

# Application Parameters
ROOT_DIR = '/storage/home/yjo5006/work/oer_rawdata/'

# Open File Map List
filelist = [tuple(f.split('/')[7:]) for f in open('rawdata_fmap.txt', 'r').read().split('\n')[:-1]]

print('ORIGINAL: ' + str(len(filelist)))
print('REDUCED: ' + str(len(list(set(filelist)))))

# Generate New Filemap
output = open('rawdata_fmap_url-redux.txt', 'w')
for x in list(set(filelist)): output.write('/'.join(x) + '\n')
output.close()
