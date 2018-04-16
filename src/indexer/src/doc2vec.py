'''
Text Preprocessing Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import nltk
import json
import string
import numpy as np
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Application Parameters
THREADS = 32


# Initialize NLTK Objects
stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

# Set PRNG Seed
np.random.seed(2342234)

# Preprocessing Function
def process(doc):
    text = open('doc')
    tokens = [stemmer.stem(t.lower()) for t in nltk.word_tokenize(text.translate(None, string.punctuation)) if t.lower() not in stopwords]
    return LabeledDocs(tokens, doc_id)

# Document Object
class LabeledDocs(object):
    def __init__(self, tokens, tag):
        self.doc = TaggedDocument(words=tokens, tags=[tag])
        self.tag = tag

class DocList(object):
    def __init__(self, docs=None):
        if docs is None: self.docs = []
        else: self.docs = docs

    def append(self, doc_obj):
        self.docs.append(doc_obj)

    def toArray(self):
        docList_arr = []
        for d in self.docs: docList_arr.append(d.doc)
        return docList_arr

    def __iter__(self):
        for d in self.docs: yield d

    def size(self):
        return len(self.docs)

# Open Metadata File
metadata = json.loads(open('oer_metadata.json', 'rb').read())

# Process Documents
p = Pool(150)
documents = DocList(p.map(process, metadata))
