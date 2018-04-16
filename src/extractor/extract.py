'''
Raw Data Content Extraction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import os
import uuid
import magic
import shutil
import textract
import subprocess as sp
from bs4 import BeautifulSoup
from boilerpipy import Extractor

# Application Paraemeters
ROOT_DIR = ''

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
            content = open(file_dir, 'rb').read()
            soup = BeautifulSoup(Extractor(content).extracted(), 'html.parser')

            # Return Content Based on Text Density Ratio
            if len(content) == 0 or len(soup.text) == 0:
                return None
            elif self.min_density < (len(soup.text) / len(content)):
                return soup.text
            else:
                return None
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

if __name__  == '__main__':
    ext = ContentExtract()
    print(ext.process('test.html'))
