'''
Raw Data Content Extraction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import os
import re
import uuid
import json
import magic
import shutil
# import textract
import subprocess as sp
from bs4 import Comment
from bs4 import BeautifulSoup
from boilerpipy import Extractor
from multiprocessing import Pool

# Application Paraemeters
ROOT_DIR = '/tmp/oer_rawtext/'
DESC_LEN = 250
THREADS = 256

class ContentExtract:
    def __init__(self, tmp_dir='./exttmp', min_density=0.1):
        # Setup Temporary Directory
        self.tmp_dir = tmp_dir
        if not os.path.isdir(self.tmp_dir): os.makedirs(self.tmp_dir)

        self.min_density = 0.1  # HTML Boilerpipe Text Density Ratio

    def __del__(self):
        shutil.rmtree(self.tmp_dir)

    def filetype(self, file_dir):
        return magic.from_file(file_dir, mime=True)

    def process(self, file_dir):
        # Extract File Type
        type = self.filetype(file_dir)

        if type == 'text/html':
            # Extract Text Content
            content = Extractor(open(file_dir, 'rb').read()).extracted()
            if content == None: return None
            soup = BeautifulSoup(content, 'html.parser')

            # Return Content Based on Text Density Ratio
            if len(content) == 0 or len(soup.text) == 0:
                return None
            elif self.min_density < (len(soup.text) / len(content)):
                return soup.text
            else:
                return None
        '''
        elif type == 'application/pdf':
            tmp_file = self.tmp_dir + '/' + str(uuid.uuid4()) + '.txt'
            print(self.tmp_dir + '/' + tmp_file)
            sp.check_call(['gs', '-sDEVICE=txtwrite', '-o', tmp_file, file_dir], shell=False, stdout=sp.PIPE)
            return open(tmp_file, 'rb').read()
        elif type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or type == 'application/msword':
            return textract.process(file_dir)
        elif type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
            return textract.process(file_dir)
        elif type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or type == 'application/vnd.ms-excel':
            return textract.process(file_dir)
        elif type == 'text/plain':
            return open(fle_dir, 'rb').read()
        elif type == 'text/rtf':
            return textract.process(file_dir)
        '''

    def extract_meta(self, file_dir):
        # Setup Metadata Dictionary
        meta = dict()
        meta['uuid'] = str(uuid.uuid4())

        # Extract HTML Content
        content = open(file_dir, 'rb').read()
        if len(content) is 0: return

        soup = BeautifulSoup(content, 'html.parser')

        # Page URL
        comments = soup.find_all(string = lambda text : isinstance(text, Comment))
        for c in comments:
            if ' Mirrored from' in c:
                meta['url'] = c.split(' ')[3]
                break

        # Document Title
        if soup.title: meta['title'] = soup.title.text
        elif 'url' in meta: meta['title'] = meta['url']
        else: meta['title'] = ''

        return meta

if __name__  == '__main__':
    # Load File Map List
    data = open('rawdata_fmap.txt', 'r').read().split('\n')[:-1]

    # Initialize Content Extraction Module
    ext = ContentExtract()
    meta_list = []

    def f(path):
        print('PROCESSING: ' + path)

        # Extract Text Information
        data = ext.process(path)
        if data is None or len(data) == 0: return

        # Extract Meta Data
        meta = ext.extract_meta(path)

        # Output Contents
        out = open(ROOT_DIR + meta['uuid'] + '.txt', 'w')
        out.write(data)
        out.close()

        # Return Metadata as Output
        return meta

    # Multiprocessing Handler
    p = Pool(THREADS)
    meta_list = p.map(f, data)
    p.close()
    
    # list(map(f, data))
    print(meta_list)

    # Write Metadata
    meta_out = open('oer_metadata.json', 'w')
    meta_out.write(json.dumps(meta_list))
    meta_out.close()
